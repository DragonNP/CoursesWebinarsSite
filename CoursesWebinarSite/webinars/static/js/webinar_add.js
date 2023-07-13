function addPhoto() {
    var photos_count = document.getElementById('photos_count');
    count = parseInt(photos_count.getAttribute('value'), 10);
    photos_count.setAttribute('value', count + 1);

    var div_row = document.createElement("div");
    div_row.setAttribute("id", "photo_"+count);
    div_row.setAttribute("class", "row mb-3");

    var div_col = document.createElement("div");
    div_col.setAttribute("class", "input-group col");

    var input = document.createElement("input");
    input.setAttribute("class", "form-control");
    input.setAttribute("type", "text");
    input.setAttribute("pattern", "(https?:\\/\\/)?(?:(?:[a-zA-Z\\u00a1-\\uffff0-9]+-?)*[a-zA-Z\\u00a1-\\uffff0-9]+)(?:\\.(?:[a-zA-Z\\u00a1-\\uffff0-9]+-?)*[a-zA-Z\\u00a1-\\uffff0-9]+)*(?:\\.(?:[a-zA-Z\\u00a1-\\uffff]{2,}))(?::\\d{2,5})?(?:\\/[^\\s]*)?");
    input.setAttribute("name", "photo_"+count);
    input.setAttribute("placeholder", "Ссылка");
    input.setAttribute("required", "");

    var div_btn = document.createElement("div");
    div_btn.setAttribute("class", "input-group-append");
    div_btn.setAttribute("required", "");

    var button = document.createElement("button");
    button.setAttribute("class", "btn btn-outline-danger");
    button.setAttribute("type", "button");
    button.setAttribute("onclick", "rmPhoto("+count+")");
    button.innerHTML = "X";

    div_btn.appendChild(button)
    div_col.appendChild(input)
    div_col.appendChild(div_btn)
    div_row.appendChild(div_col)

    document.getElementById("photos").appendChild(div_row);
}
function rmPhoto(count) {
    document.getElementById("photo_"+count).remove();
}
function addFile() {
    var files_count = document.getElementById('files_count');
    count = parseInt(files_count.getAttribute('value'), 10);
    files_count.setAttribute('value', count + 1);

    var div_row = document.createElement("div");
    div_row.setAttribute("id", "file_"+count);
    div_row.setAttribute("class", "row mb-3");

    var div_col = document.createElement("div");
    div_col.setAttribute("class", "input-group col");

    var input_name = document.createElement("input");
    input_name.setAttribute("class", "form-control col");
    input_name.setAttribute("type", "text");
    input_name.setAttribute("name", "file_name_"+count);
    input_name.setAttribute("placeholder", "Название");
    input_name.setAttribute("required", "");

    var input_url = document.createElement("input");
    input_url.setAttribute("class", "form-control col-5");
    input_url.setAttribute("type", "text");
    input_url.setAttribute("pattern", "(https?:\\/\\/)?(?:(?:[a-zA-Z\\u00a1-\\uffff0-9]+-?)*[a-zA-Z\\u00a1-\\uffff0-9]+)(?:\\.(?:[a-zA-Z\\u00a1-\\uffff0-9]+-?)*[a-zA-Z\\u00a1-\\uffff0-9]+)*(?:\\.(?:[a-zA-Z\\u00a1-\\uffff]{2,}))(?::\\d{2,5})?(?:\\/[^\\s]*)?");
    input_url.setAttribute("name", "file_url_"+count);
    input_url.setAttribute("placeholder", "Ссылка");
    input_url.setAttribute("required", "");

    var div_btn = document.createElement("div");
    div_btn.setAttribute("class", "input-group-append");

    var button = document.createElement("button");
    button.setAttribute("class", "btn btn-outline-danger");
    button.setAttribute("type", "button");
    button.setAttribute("onclick", "rmFile("+count+")");
    button.innerHTML = "X";

    div_btn.appendChild(button)
    div_col.appendChild(input_name)
    div_col.appendChild(input_url)
    div_col.appendChild(div_btn)
    div_row.appendChild(div_col)

    document.getElementById("files").appendChild(div_row);
}
function rmFile(count) {
    document.getElementById("file_"+count).remove();
}
function addMusic() {
    var musics_count = document.getElementById('musics_count');
    count = parseInt(musics_count.getAttribute('value'), 10);
    musics_count.setAttribute('value', count + 1);

    var div_row = document.createElement("div");
    div_row.setAttribute("id", "music_"+count);
    div_row.setAttribute("class", "row mb-3");

    var div_col = document.createElement("div");
    div_col.setAttribute("class", "input-group col");

    var input = document.createElement("input");
    input.setAttribute("class", "form-control");
    input.setAttribute("type", "text");
    input.setAttribute("pattern", "(https?:\\/\\/)?(?:(?:[a-zA-Z\\u00a1-\\uffff0-9]+-?)*[a-zA-Z\\u00a1-\\uffff0-9]+)(?:\\.(?:[a-zA-Z\\u00a1-\\uffff0-9]+-?)*[a-zA-Z\\u00a1-\\uffff0-9]+)*(?:\\.(?:[a-zA-Z\\u00a1-\\uffff]{2,}))(?::\\d{2,5})?(?:\\/[^\\s]*)?");
    input.setAttribute("name", "music_"+count);
    input.setAttribute("placeholder", "Ссылка");
    input.setAttribute("required", "");

    var div_btn = document.createElement("div");
    div_btn.setAttribute("class", "input-group-append");
    div_btn.setAttribute("required", "");

    var button = document.createElement("button");
    button.setAttribute("class", "btn btn-outline-danger");
    button.setAttribute("type", "button");
    button.setAttribute("onclick", "rmMusic("+count+")");
    button.innerHTML = "X";

    div_btn.appendChild(button)
    div_col.appendChild(input)
    div_col.appendChild(div_btn)
    div_row.appendChild(div_col)

    document.getElementById("musics").appendChild(div_row);
}
function rmMusic(count) {
    document.getElementById("music_"+count).remove();
}
