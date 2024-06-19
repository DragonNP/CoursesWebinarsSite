let account_url = ''
let account_email = ''
let account_password = ''

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function save_list(event) {
    event.preventDefault();
    const list = serializeFormList(document.getElementById("form_list"));

    let js = {}
    let i = 0;
    while (true) {
        if (list[i]) {
            module = recursion(list, i+'.');
            js[list[i][0]] = [module, list[i][1]];
            i++;
        }
        else {
            break;
        }
    }
    body = {'account': {'url': account_url, 'email': account_email, 'password': account_password}, 'data': js}
    url = '/api/v1/curses/get_course';
    const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Content-Length': body.length,
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(body),
    });
    const data = await response.json();
//    if (data['success'] == false) {
//      document.getElementById("alert").innerHTML = data['errorMessage'];
//      document.getElementById("div_alert").style.display = "inline";
//    }
//    else {
//        await show_list_courses(data['data']);
//    }
}

function recursion(list, domen) {
    let js = {}
    let i = 0;
    while (true) {
        if (list[domen + i]) {
            if (list[domen + i][1] == 'module') {
                modules = recursion(list, domen + i+'.');
                js[list[domen + i][0]] = [modules, list[domen + i][1]]
            }
            else {
                js[list[domen + i][0]] = [list[domen + i][2], list[domen + i][1]]
            }
            i++;
        }
        else {
            return js;
        }
    }
}

function toggleButton() {
  const submit = document.getElementById('submit')
  submit.classList.toggle('d-none')

  const loader = document.getElementById('loader_btn')
  loader.classList.toggle('d-none')
}

function serializeFormLogin(formNode) {
  const { elements } = formNode
  params = {}
  Array.from(elements)
    .forEach((element) => {
      const { name, value } = element
      if (name != '') {
        params[name] = [value]
      }
    })
  return params
}

function serializeFormList(formNode) {
  const { elements } = formNode
  params = {}
  Array.from(elements)
    .forEach((element) => {
      const { name, value } = element
      if (name != '') {

          input = document.getElementsByName(name)[0]
          data_type = input.getAttribute("data-type");

          if (data_type == 'lesson') {
                data_id = input.getAttribute("data-id");
                params[name] = [value, data_type, data_id]
            }
          else {
           params[name] = [value, data_type]
            }
      }
    })
  return params
}

async function form_send(form){
    document.getElementById("div_alert").style.display = "none";
    url = '/api/v1/curses/get_course'
    params = serializeFormLogin(form);

    toggleButton();
    const response = await fetch(url + '?' + new URLSearchParams(params));
    const data = await response.json();
    toggleButton();

    if (data['success'] == false) {
      document.getElementById("alert").innerHTML = data['errorMessage'];
      document.getElementById("div_alert").style.display = "inline";
    }
    else {
        await show_list_courses(data['data']);
    }
}

function show_list_courses(data) {
    account_url = document.getElementById('url').value
    account_email = document.getElementById('email').value
    account_password = document.getElementById('password').value

    document.getElementById("course_add").remove();

    form = document.createElement('form');
    form.setAttribute('class', 'form-signin');
    form.setAttribute('id', 'form_list');
    form.addEventListener('submit', save_list);

    btn = document.createElement('button');
    btn.setAttribute('class', 'btn btn-lg btn-success btn-block mb-3');
    btn.setAttribute('type', 'submit');
    btn.innerHTML = 'Импортировать';
    form.appendChild(btn);

    ul = document.createElement("ul");
    ul.setAttribute("id", "courses");
    form.appendChild(ul);

    document.getElementById('content').appendChild(form);
    var i = 0;
    for(var k in data) {
       ul.appendChild(add_module(k, data[k], i, 0));
       i += 1;
    }
}

form = document.getElementById('course_add');
form.addEventListener('submit', function (event) {
    event.preventDefault()
    if (!form.checkValidity()) {
      event.stopPropagation();
      document.getElementById("alert").innerHTML = "Пожалуйста, исправьте введенные данные";
      document.getElementById("div_alert").style.display = "inline";
    }
    else {
        form_send(form);
    }
    form.classList.add('was-validated')
}, false)
