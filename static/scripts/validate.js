function isValid(input) {
    return input.validity.valid;
}

function hasValidationFail(inputsList) {
    return inputsList.some(input => {
        return !input.validity.valid;
    });
}

function toogleSubmitButton(inputsList, button, inactiveButtonClass) {
    if(hasValidationFail(inputsList)){
        button.classList.add(inactiveButtonClass);
        button.disabled = true;
    }else{
        button.classList.remove(inactiveButtonClass);
        button.disabled = false;
    }
}

function showErrorMsg(form, input, errorstrMsg, inputErrorClass) {
    const errorSpan = form.querySelector(`.${input.id}-error`);
    input.classList.add(inputErrorClass);
    errorSpan.textContent = errorstrMsg;
}

function hideErrorMsg(form, input, inputErrorClass) {
    input.classList.remove(inputErrorClass);
    form.querySelector(`.${input.id}-error`).textContent = '';
}

function changeValidateState(form, input, inputErrorClass){
    if(!isValid(input)) {
        showErrorMsg(form, input, input.validationMessage, inputErrorClass);
    }else{
        hideErrorMsg(form, input, inputErrorClass);
    }
}

function setInputListeners(form, validSelectors) {
    const inputsList = Array.from(form.querySelectorAll(`.${validSelectors.inputSelector}`));
    const submitButton = form.querySelector(`.${validSelectors.submitButtonSelector}`);
    toogleSubmitButton(inputsList, submitButton, validSelectors.inactiveButtonClass);
    inputsList.forEach(input =>{
        input.addEventListener('input', (evt) => {
            changeValidateState(form, input, validSelectors.inputErrorClass);
            toogleSubmitButton(inputsList, submitButton, validSelectors.inactiveButtonClass);
        });
        input.addEventListener('change', (evt) =>{
            changeValidateState(form, input, validSelectors.inputErrorClass);
            toogleSubmitButton(inputsList, submitButton, validSelectors.inactiveButtonClass);
        });
    });
}

function enableValidation(validSelectors) {
    Array.from(document.forms).forEach(form =>{
        form.addEventListener('submit', (evt)=>{
            evt.preventDefault();
        });
        setInputListeners(form, validSelectors);
    });
}
// вызовы функций

enableValidation({
    formSelector: 'popup__form',
    inputSelector: 'popup__input',
    submitButtonSelector: 'popup__button-save',
    inactiveButtonClass: 'popup__button-save_inactive',
    inputErrorClass: 'popup__input_type_error',
    errorClass: 'popup__input-error-info'
});