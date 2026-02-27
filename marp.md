---
marp: true
# theme: gaia
theme: custom
header: 'My Presentation'
footer: hello
paginate: true
---

<!-- ![bg](figure.jpg) -->

<!-- _class: lead title -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

# Hello Marp

--- 

## Ví dụ sử dụng màu **cam** (#f54914)

- Link: [Click here](https://example.com)
- Marked text: ==Văn bản được highlight==
- Heading với **text in đậm**

---
### Heading với **orange** color

Normal text stays black, but **bold in headings** is orange!

---

## Slide với 2 cột

<style scoped>
.columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
</style>

<div class="columns">

<div>

- Item 1
- Item 2

</div>

<div>

- Item A
- Item B

</div>

</div>

---

## Slide với 2 cột có ảnh

<div class="columns">

<div>

- Item 1
- Item 2

</div>

<div>

![](figure.jpg)

</div>

</div>
