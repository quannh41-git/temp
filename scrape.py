from main import WQSession
import time
import logging
import csv
import pandas as pd
from concurrent.futures import as_completed, ThreadPoolExecutor
from threading import current_thread

team_params = {
    'status':               'ACTIVE',
    'members.self.status':  'ACCEPTED',
    'order':                '-dateCreated'
}

OFFSET, LIMIT = 0, 30
def get_link(x):
    return f'https://api.worldquantbrain.com/users/self/alphas?limit={LIMIT}&offset={x}&stage=IS%1fOS&is.sharpe%3E=1.25&is.turnover%3E=0.01&is.fitness%3E=1&status=UNSUBMITTED&order=-dateCreated&hidden=false'

wq = WQSession()

# XỬ LÝ LẤY TEAM AN TOÀN CHO CẢ CÁ NHÂN VÀ ĐỒNG ĐỘI
r = wq.get('https://api.worldquantbrain.com/users/self/teams', params=team_params).json()
results = r.get('results', [])
if results:
    team_id = results[0]['id']
    print('Đã lấy thông tin team:', team_id)
else:
    team_id = None
    print('Không tìm thấy thông tin team. Đang chạy ở chế độ Tài Khoản Cá Nhân.')

def scrape(result):
    thread = current_thread().name
    alpha = result['regular']['code']
    settings = result['settings']
    aid = result['id']
    
    passed = sum(check['result'] == 'PASS' for check in result['is']['checks'])
    failed = sum(check['result'] in ['FAIL', 'ERROR'] for check in result['is']['checks'])
    if failed != 0: 
        return -1

    # Sử dụng endpoint chính thức của Alpha thay vì đường dẫn /check không ổn định
    while True:
        check_r = wq.get(f'https://api.worldquantbrain.com/alphas/{aid}')
        if check_r.content:
            try:    
                checks = check_r.json()['is']['checks']
                break
            except: 
                pass
        time.sleep(2.5)
        
    if not all(check['result'] == 'PASS' for check in checks): 
        return -1
        
    # Gán Sharpe Ratio làm giá trị proxy cho 'after' để hàng đợi sắp xếp thứ tự tối ưu
    score = {
        'before': 0.0,
        'after': result.get('is', {}).get('sharpe', 0.0)
    }
    
    # Lấy thông số SELF_CORRELATION an toàn tránh lỗi IndexError
    self_corr_checks = [check['value'] for check in checks if check['name'] == 'SELF_CORRELATION']
    score['max_corr'] = self_corr_checks[0] if self_corr_checks else -1.0

    # Gộp cấu hình cài đặt simulation vào kết quả
    score |= settings
    
    def clean(alpha):
        lines = alpha.split('\n')
        new_lines = []
        for line in lines:
            while '#' in line:
                line = line[:line.find('#')]
                line = line.strip()
            line = line.strip()
            if line: new_lines.append(line)
        new_alpha = ''.join(new_lines)
        return new_alpha
        
    score['passed'] = passed
    score['alpha'] = clean(alpha)
    score['link'] = f'https://platform.worldquantbrain.com/alpha/{aid}'
    
    logging.info(f'{thread} -- Thành công! -- {score}')
    return score

ret = []
SCRAPE_FN = f'data/alpha_scrape_result_{int(time.time())}.csv'

for handler in logging.root.handlers:
    logging.root.removeHandler(handler)
logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s: %(message)s', filename=SCRAPE_FN.replace('csv', 'log'))

with open(SCRAPE_FN, 'w', newline='') as c:
    writer = csv.DictWriter(c, fieldnames='before,after,max_corr,instrumentType,region,universe,delay,decay,neutralization,truncation,pasteurization,unitHandling,nanHandling,language,visualization,passed,alpha,link'.split(','))
    writer.writeheader()
    c.flush()
    with ThreadPoolExecutor(max_workers=10) as executor:
        try:
            while True:
                r = wq.get(get_link(OFFSET)).json()
                logging.info(f'Đã lấy thông tin của các alpha #{OFFSET+1}-#{OFFSET+LIMIT}')
                for f in as_completed([executor.submit(scrape, result) for result in r['results']]):
                    res = f.result()
                    if res != -1:
                        ret.append(res)
                        writer.writerow(res)
                        c.flush()
                OFFSET += LIMIT
                if not r['next']: 
                    break
        except Exception as e:
            logging.info(f'{type(e).__name__}: {e}')
            try:    
                logging.info(r.content)
            except: 
                pass

if ret:
    pd.DataFrame(ret).sort_values(by=['after', 'max_corr'], ascending=[False, True]).to_csv(SCRAPE_FN, index=False)
    print(f'Hoàn tất! Hãy chạy lệnh sau để thực hiện nộp alpha: \npython submit_alphas.py {SCRAPE_FN}')
else:
    print('Không tìm thấy alpha chưa nộp nào đủ điều kiện vượt qua vòng IS.')
