var engword = [], rusword = [], errors = [], index = 0, index_round = 1, error_count = 0, is_err_work = 0;
revers_word = 0;
var select_value = 0;
var select = document.getElementById("number_repetitions_Sel");
select_value = select.options[select.selectedIndex].value;


document.getElementById('count_errors').innerHTML = error_count.toString();


function new_word_tranclste() {
    const word_new_translate = new Map();
    let rusword_new = document.getElementById('input_word_learn_new_tranclate').value.toLowerCase().trim();
    var span_text_new_translate = document.getElementsByClassName("new_learn_rus_word");


    document.getElementById('input_word_learn_new_tranclate').value = "";
    document.getElementById('input_word_learn_new_tranclate').setAttribute('placeholder', rusword_new.charAt(0).toUpperCase() + rusword_new.slice(1));
    document.getElementById('input_word_learn_new_label').value = rusword_new.charAt(0).toUpperCase() + rusword_new.slice(1);
    document.getElementById('input_word_learn_new_label').innerHTML = rusword_new.charAt(0).toUpperCase() + rusword_new.slice(1);
    for (var i = 0; i < span_text_new_translate.length; i++) {
        if (span_text_new_translate[i].textContent.toLowerCase().trim() === rusword[index].toLowerCase().trim()) {
            span_text_new_translate[i].innerHTML = rusword_new.charAt(0).toUpperCase() + rusword_new.slice(1);
            break;
        }
    }
    rusword[index] = rusword_new;


    word_new_translate.set(engword[index], rusword_new);
    const json = JSON.stringify(Object.fromEntries(word_new_translate));
    Json_send_new_translate(json);                        //Отправляем  анг и новое русское слово.

}

function finaly_block() {
    document.getElementById('input_word_learn_new').setAttribute('readonly', 'true');
    document.getElementById('number_repetitions_Sel').setAttribute('disabled', 'true');
    document.getElementById('checkbox_err_work').setAttribute('disabled', 'true');
    document.getElementById('btn_new_tranclate').setAttribute('disabled', 'true');
    document.getElementById('input_word_learn_new_tranclate').setAttribute('readonly', 'true');
    document.getElementById('collapse_learn_words_new_btn').removeAttribute('class');
    document.getElementById('input_word_learn_new_tranclate').removeAttribute('placeholder');
    document.getElementById('collapse_learn_words_new_btn').setAttribute('class', 'btn btn-secondary form-control');





    let OK_and_typo_button = document.getElementsByClassName('err_ok_prompt_new_learn_btn');
    let revers_words_button = document.getElementsByClassName('revers_words');

    for (let i = 0; i < OK_and_typo_button.length; i++) {
        OK_and_typo_button[i].setAttribute('class', 'btn btn-secondary err_ok_prompt_new_learn_btn');
        OK_and_typo_button[i].setAttribute('disabled', 'true');
        revers_words_button[i].setAttribute('class', 'btn btn-secondary revers_words');
        revers_words_button[i].setAttribute('disabled', 'true');
    }





}

function next_Word(i, select_value) {
    var str = rusword[i];
    //console.log("rusword[i] ==", rusword[i]);
    var str_eng = engword[i];
    var word_rus = str.charAt(0).toUpperCase() + str.slice(1);
    var word_eng = str_eng.charAt(0).toUpperCase() + str_eng.slice(1);
    let progress_bar_total = (100 / select_value) * index_round;
    let progres_bar_round = (100 / engword.length) * index;

    document.getElementById("input_word_learn_new_label").innerHTML = word_rus;
    document.getElementById("input_word_learn_new_label_tranclate").innerHTML = "Новый перевод слова";
    document.getElementById("input_word_learn_new_label").value = word_rus;
    document.getElementById("input_word_learn_new_label_tranclate").setAttribute('value', word_eng);
    document.getElementById("input_word_learn_new_tranclate").setAttribute('placeholder', word_rus);


    document.getElementById('current_round_progress').removeAttribute('style');
    document.getElementById('current_round_progress').setAttribute('style', 'width:' + progres_bar_round + '%');

    document.getElementById('total_progress').removeAttribute('style');
    document.getElementById('total_progress').setAttribute('style', 'width:' + progress_bar_total + '%');


}

function ajax_get(url, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {

            try {
                var data = JSON.parse(xmlhttp.responseText);
            } catch (err) {

                return;
            }
            callback(data);
        }
    };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

ajax_get(url_get_new_words, function (data) {
        var p = document.getElementById("new_learn_eng_word_p");

        if (data["words"].length === 0) {
            p.innerHTML = "<p><span class='new_learn_eng_word'>" + "Новых слов" + ":</span><span class='new_learn_rus_word'>" + "Нет" + "</span> </p>";
            document.getElementById("input_word_learn_new_label").innerHTML = "Новых слов нет";
            document.getElementById("input_word_learn_new_label").value = "Новых слов нет";
            document.getElementById("collapse_learn_words_new").removeAttribute('class');
            document.getElementById("collapse_learn_words_new").setAttribute('class', 'collapse');
            finaly_block();

            return 0;
        } else {
            for (var i = 0; i < data["words"].length; i++) {
                engword[i] = data["words"][i]["engword"];
                rusword[i] = data["words"][i]["rusword"];
                let engword_tmp = engword[i].charAt(0).toUpperCase() + engword[i].slice(1);
                let rusword_tmp = rusword[i].charAt(0).toUpperCase() + rusword[i].slice(1);
                errors[i] = 0;
                p.innerHTML += "<p><span class='new_learn_eng_word'>" + engword_tmp + ":</span><span class='new_learn_rus_word'>" + rusword_tmp + "</span> </p>";
            }


            next_Word(0, select_value);
        }

    }
);


async function request(url, data, csrftoken) {
    //console.log(data);
    //console.log(JSON.stringify(data));
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
        },
        body: data,
    })
    const result = await response.text();
    //console.log('Ответ сервера: ', result);
    return result
}

async function Json_send(data) {
    const url = url_push_new_words;
    const csrftoken = csrftoken_new_words;
    const result = await request(url, data, csrftoken);
    //console.log('Ответ сервера: ', result);
}

async function Json_send_new_translate(data) {
    const url = url_push_new_translate;
    const csrftoken = csrftoken_new_words;
    const result = await request(url, data, csrftoken);
    //console.log('Ответ сервера: ', result);
}


function select_button_click() {
    select_value = select.options[select.selectedIndex].value;
    if (select_value < index_round) {
        select.selectedIndex = index_round - 1;
    }
}

function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

function button_word_click() {
    var engword_input = document.getElementById('input_word_learn_new').value.toLowerCase();
    engword_input = engword_input.trim();

    for (let i = 0; i < errors.length; i++) {
        //console.log("errors = ", errors[i]);
    }

    //console.log("index = ", index);
    //console.log("index_round = ", index_round);
    //console.log("error_count = ", error_count);
    //console.log("errors.length = ", errors.length);
    //console.log("select_value = ", select_value);

    if (engword_input === "") {      //подсказка
        document.getElementById('input_word_learn_new').setAttribute('placeholder', engword[index]);
        return 0;
    }

    if (engword_input !== engword[index]) {           // Ошибка в написании is-invalid
        document.getElementById('input_word_learn_new').removeAttribute('class');
        document.getElementById('input_word_learn_new').setAttribute('class', 'form-control is-invalid');
        error_count++;
        document.getElementById('count_errors').innerHTML = error_count.toString();
        errors[index]++;
    }

    if (engword_input === engword[index]) {     //проверка на правильность написания прошла, все верно
        if (index < rusword.length - 1) {

            index++;
            document.getElementById('input_word_learn_new').value = "";

            next_Word(index, select_value);

            document.getElementById('input_word_learn_new').setAttribute('placeholder', '');
            document.getElementById('input_word_learn_new').removeAttribute('class');
            document.getElementById('input_word_learn_new').setAttribute('class', 'form-control');


            return 0;
        }


        if ((index === rusword.length - 1) && (select_value > index_round)) {      //новый круг
            index_round++;
            document.getElementById('number_repetitions_now').innerHTML = index_round.toString();

            index = 0;

            let engword_tmp = "";
            let rusword_tmp = "";


            for (let i = 0; i < engword.length; i++) {
                let j = getRndInteger(0, engword.length);

                engword_tmp = engword[j]
                rusword_tmp = rusword[j]

                engword[j] = engword[i];
                rusword[j] = rusword[i];

                engword[i] = engword_tmp;
                rusword[i] = rusword_tmp
            }

            next_Word(index, select_value);
            document.getElementById('input_word_learn_new').value = "";
        }

        if ((index === rusword.length - 1) && (select_value >= index_round)) {      //закончено последнее слово
            document.getElementById('input_word_learn_new').value = "";
            document.getElementById('current_round_progress').removeAttribute('style');
            document.getElementById('current_round_progress').setAttribute('style', 'width:' + 100 + '%');

            document.getElementById('total_progress').removeAttribute('style');
            document.getElementById('total_progress').setAttribute('style', 'width:' + 100 + '%');

            const word_err = new Map();
            let count_err = 0;

            for (let i = 0; i < errors.length; i++) {
                let arr = [errors[i].toString(), select_value.toString()];
                word_err.set(engword[i], arr);
                if (errors[i] > 0) {
                    count_err++;
                }
            }
            if (count_err > 0) {
                word_err.set("no_err", "1");
            } else {
                word_err.set("no_err", "0");
            }

            if (is_err_work === 0) {
                const json = JSON.stringify(Object.fromEntries(word_err));
                //console.log(json);
                if (revers_word === 0) {   // если перевод не перевернут
                    Json_send(json);
                }//Отправляем слова и кол-во ошибок, далее работа над ошибками.
            }
            if ((document.getElementById('checkbox_err_work').checked) && (error_count !== 0)) {

                index = 0;
                index_round = 1;
                error_count = 0;
                is_err_work = 1;
                var engword_tmp = [], rusword_tmp = [];
                for (let i = 0; i < errors.length; i++) {
                    if (errors[i] > 0) {
                        engword_tmp.push(engword[i]);
                        rusword_tmp.push(rusword[i]);
                        errors[i] = 0;
                    }

                }
                engword = engword_tmp;
                rusword = rusword_tmp;

                select.value = 2;
                select_value = select.value;
                next_Word(index, select_value);
                return 0;
            }
            document.getElementById('input_word_learn_new').removeAttribute('class');
            document.getElementById('input_word_learn_new_label').removeAttribute('class');

            document.getElementById('input_word_learn_new').setAttribute('class', 'form-control is-valid');
            document.getElementById('input_word_learn_new_label').setAttribute('class', 'form-control is-valid');
            document.getElementById('input_word_learn_new_label').innerHTML = "На этом все!";
            document.getElementById('input_word_learn_new_label').value = "На этом все!";


            finaly_block();
        }

    }


}

function input_is_invalid_click() {
    let el = document.getElementById('input_word_learn_new');
    el.setAttribute('type', 'text');
    if (el.getAttribute('class') === 'form-control is-invalid') {
        el.value = "";
        el.removeAttribute('class');
        el.setAttribute('class', 'form-control');
    }
}

function enter_down(e) {
    if (e.keyCode === 13) {
        e.preventDefault(); // Ensure it is only this code that rusn

        button_word_click();
    }
}


function button_revers_word_click() {
    if (revers_word === 0) {
        revers_word = 1;
    } else {
        revers_word = 0;
    }
    //console.log("revers_word = ", revers_word);

    let engword_tmp = [], rusword_tmp = [];
    for (var i = 0; i < engword.length; i++) {
        engword_tmp.push(engword[i]);
        rusword_tmp.push(rusword[i]);
    }
    for (var i = 0; i < engword.length; i++) {  //самый топовый костыль на свете
        engword[i] = rusword_tmp[i];
        rusword[i] = engword_tmp[i];
    }
    next_Word(index, select_value);
    return false
}

addEventListener("keydown", enter_down);

function button_typo_click() {
    error_count = error_count - 1;
    errors[index]--;
    document.getElementById('input_word_learn_new').removeAttribute('class');
    document.getElementById('input_word_learn_new').setAttribute('class', 'form-control');
    document.getElementById('input_word_learn_new').value = "";

    document.getElementById('count_errors').innerHTML = error_count.toString();
}