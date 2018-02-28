'use strict';

const sendPost = (url, payload, csrf) => {
    return new Promise((success) => {
            const req = new XMLHttpRequest();
            req.open("POST", url, true);
            req.setRequestHeader('contentType', 'application/json; charset=utf-8');
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
form.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = {};
    data.userId = form.querySelector('[name="user"]').value;
    data.inn = form.querySelector('[name="inn"]').value;
    data.amount = form.querySelector('[name="amount"]').value;
    sendPost('/transaction', data, form.querySelector('[name="csrfmiddlewaretoken"]').value).then((response) => {
        const data = JSON.parse(response);
        if(data.error){
            errorRow.innerHTML = data.message;
        }else{
            form.querySelector('[name="inn"]').value = '';
            form.querySelector('[name="amount"]').value = '';
            errorRow.innerHTML = data.message;
        }
    })
});