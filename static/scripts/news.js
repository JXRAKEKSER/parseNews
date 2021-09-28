const dataObj = {}
const title = document.querySelector('.news__title');
const image = document.querySelector('.news__image');
const date = document.querySelector('.news__date');
const text = document.querySelector('.news__text');
function getData() {
    const dataTemplate = document.querySelector('#news-detail').content.cloneNode(true);
    const dataObj = {}
     Array.from(dataTemplate.children).forEach(child => {

        dataObj[`${child.classList[0]}`] = child.textContent;

    });
    return dataObj;
}

function setContent(data){
    title.textContent = data.title;
    image.src = data.image;
    image.alt = `${data.title}`;
    date.textContent = data.date;
    text.textContent = data.text;
}

setContent(getData());








