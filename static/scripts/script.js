
// блок объявления и инициализации общих элементов(контейнеры, секции и т.п. семантически общие вещи)
const elementsContainer = document.querySelector('.elements');


// блок объявления и инициализации элементов добавления места
const addMestoButton = document.querySelector('.profile__button-add');
const addMestoPopup = document.querySelector('.popup_type_card-add');
const closeAddMestoPopupButton = document.querySelector('.popup_type_card-add .popup__button-close');
const interval = document.querySelector('input[name=mestoName]');
const formAddMestoContainer = document.querySelector('.popup_type_card-add .popup__form');
// блок объявления и инициализации элементов просмотра картинки
const mestoPhotoPopup = document.querySelector('.popup_type_picture');
const closeMestoPhotoPopupButton =  document.querySelector('.popup_type_picture .popup__button-close');

//блок переменных управления страницей
const checkbox = document.querySelector('.page-controll-form__checkbox');
let intervalValue = 0;
const storage = window.localStorage;
const convertToBool = (stringValue) => {
    if(stringValue === 'true'){
        return true;
    }else{
        return false;
    }
}
checkbox.checked = convertToBool(storage.getItem('check'));

checkbox.addEventListener('change', () => {
    if(checkbox.checked){
        openPopup(addMestoPopup);
        storage.setItem('check', 'true');
        console.log(storage.getItem('check'))
    }else{
        storage.setItem('check', 'false');
        console.log(storage.getItem('check'))
    }
});

let reloadByInterval = setInterval(() => {
    if(convertToBool(storage.getItem('check')) === true && Number(storage.getItem('interval')) >= 5 && !addMestoPopup.classList.contains('popup_opened')){
        window.location.reload();
    }else{

    }
}, Number(storage.getItem('interval')));

reloadByInterval;

function getData(){
    const dataTemplate = document.querySelector('#info').content;
    const nodes = dataTemplate.querySelectorAll('.node');
    const data = Array.from(nodes).map(node =>{
        const dataObj ={};
        Array.from(node.children).forEach(item =>{
            dataObj[`${item.classList[0]}`] = item.textContent;
        });
        return dataObj;
    });
    return data;


}


function  createCard(cardData) {

    const cardTemplate = document.querySelector('#card').content;
    const newCard = cardTemplate.querySelector('.element').cloneNode(true);
    newCard.querySelector('.element__photo').src = cardData.image;
   // newCard.querySelector('.element__photo').alt = `Фото ${cardData.name}`;
    newCard.querySelector('.element__title').textContent = cardData.title;
    newCard.querySelector('.element__date').textContent = cardData.date;

    newCard.querySelector('a').href = `/news/${cardData.url.slice(24)}`;
    setCardEventListenets(newCard);
    return newCard;
}

function preloadCards(data) {


    data.forEach((dataItem) => {
        //renderCard инициализируется в блоке общих переменных
        elementsContainer.append(createCard(dataItem));

    });

}

//функция очистки данных внутри попапа
function clearFormInputs(popup) {
    //проверка на наличие формы в попапе, чтобы не возникало ошибки при закрытии попапа просмотра фотографий
    if(popup.querySelector('form')) {
        const form = popup.querySelector('.popup__form');
        form.reset();
    }

}
// открытие попапа
 function openPopup(popup) {
    interval.value = storage.getItem('interval');
    popup.classList.add('popup_opened');
    document.querySelector('.page').addEventListener('keydown', closePopupByKeyboard);

};
//закрытие попапа
function closePopup (popup) {
    popup.classList.remove('popup_opened');
    document.querySelector('.page').removeEventListener('keydown', closePopupByKeyboard);
    const inputsList = Array.from(popup.querySelectorAll('.popup__input'));

    //toogleSubmitButton(inputsList, popup.querySelector('.popup__button-save'), 'popup__button-save_inactive');
}





function setCardEventListenets(card) {
    const likeBtn = card.querySelector('.element__like');
    likeBtn.addEventListener('click', addLike);
    const removeBtn = card.querySelector('.element__trash');
    removeBtn.addEventListener('click', removeMestoCard);
    const photoOpener = card.querySelector('.element__photo');
    photoOpener.addEventListener('click', openWithPhoto);
}


// функция добавления карточки

function addMestoCard(evt) {
    evt.preventDefault();

    console.log(interval.value);
    intervalValue = parseInt(interval.value);
    storage.setItem('interval', `${intervalValue}`);
    console.log(intervalValue)
    const inputsList = Array.from(evt.target.closest('.popup__form').querySelectorAll('.popup__input'));
   // toogleSubmitButton(inputsList, evt.target.closest('.popup__form').querySelector('.popup__button-save'), 'popup__button-save_inactive');
    closePopup(addMestoPopup);
};

//функция удаления карточки
function removeMestoCard(evt) {
    if(evt.target.classList.contains('element__trash')) {
        const removeElement = evt.target.closest('.element');
        removeElement.querySelector('.element__like').removeEventListener('click', addLike);
        removeElement.querySelector('.element__trash').removeEventListener('click', removeMestoCard);
        removeElement.querySelector('.element__photo').removeEventListener('click', openWithPhoto);

        removeElement.remove();
    }

}

//функция проставления лайков
function addLike(evt) {
    if(evt.target.classList.contains('element__like')){
        evt.target.classList.toggle('element__like_active');
    }
}

function openWithPhoto(evt) {
        if(evt.target.classList.contains('element__photo')){
            mestoPhotoPopup.querySelector('.popup__photo').src = evt.target.src;
            mestoPhotoPopup.querySelector('.popup__photo-name').textContent = evt.target.closest('.element').querySelector('.element__title').textContent;
            mestoPhotoPopup.querySelector('.popup__photo').alt = `Фото ${mestoPhotoPopup.querySelector('.popup__photo-name').textContent}`;
            openPopup(mestoPhotoPopup);
        }


}

// вызов функции загрузки дефолтных карт
preloadCards(getData());


// блок слушателей кнопок
closeAddMestoPopupButton.addEventListener('click', () => closePopup(addMestoPopup));
formAddMestoContainer.addEventListener('submit', addMestoCard);



document.querySelector('.page').addEventListener('click', (evt) => {
   if(evt.target.classList.contains('popup')){
       closePopup(evt.target);
   }
});

function closePopupByKeyboard(evt){
    if(evt.key === "Escape"){
        closePopup(document.querySelector('.popup_opened'));
    }

}



closeMestoPhotoPopupButton.addEventListener('click', () => closePopup(mestoPhotoPopup));
