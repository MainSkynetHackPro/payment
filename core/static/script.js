'use strict';

const sendPost = (url, payload, csrf) => {
    return new Promise((success) => {
            const req = new XMLHttpRequest();
            req.open("POST", url, true);
            req.setRequestHeader('Content-Type', 'application/json; charset=utf-8');
            req.setRequestHeader('X-CSRFToken', csrf);
            req.addEventListener('load', () => {
                if(req.status < 400){
                    success(req.responseText);
                }
            });
            req.send(JSON.stringify(payload));
        });
};

const form = document.getElementsByClassName('payment-form')[0];
const errorRow = document.getElementsByClassName('error-row')[0];
const clearErrors = () => {
    const errorFields = Array.from(document.getElementsByClassName('error'));
    errorFields.map((item) => {
        item.innerHTML = '';
    })
};
form.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = {};
    data.userId = form.querySelector('[name="user"]').value;
    data.inn = form.querySelector('[name="inn"]').value;
    data.amount = form.querySelector('[name="amount"]').value;
    sendPost('/transaction', data, form.querySelector('[name="csrfmiddlewaretoken"]').value).then((response) => {
        const data = JSON.parse(response);
        clearErrors();
        if(data.error){
            for(let index in data.error){
                form.getElementsByClassName(`error-${index}`)[0].innerHTML = data.error[index];
            }
        }else{
            form.querySelector('[name="inn"]').value = '';
            form.querySelector('[name="amount"]').value = '';
        }
    })
});