function add_lesson(k, url, r, ls_index, data_id) {
    var li = document.createElement("li");
    li.setAttribute("id", 'li_' + r + (ls_index));

    var input = document.createElement("input");
    input.value = k;
    input.setAttribute("name", r + (ls_index));
    input.setAttribute("id", 'input_' + r + (ls_index));
    input.setAttribute("class", "form-control border border-primary");
    input.setAttribute("type", "text");
    input.setAttribute("data-type", "lesson");
    input.setAttribute("data-id", data_id);
    input.setAttribute("placeholder", "Урок");
    input.setAttribute("required", "");

    var div_group = document.createElement("div");
    div_group.setAttribute("class", "input-group mb-1");

    var div_group_append = document.createElement("div");
    div_group_append.setAttribute("class", "input-group-append");

    var btn_down = document.createElement("button");
    btn_down.setAttribute("class", "btn btn-outline-primary");
    btn_down.setAttribute("type", "button");
    btn_down.setAttribute("id", 'down_' + r + (ls_index));
    btn_down.setAttribute("onclick", "down('" + (r + (ls_index)) + "')");
    btn_down.innerHTML = "&darr;";

    var btn_up = document.createElement("button");
    btn_up.setAttribute("class", "btn btn-outline-primary");
    btn_up.setAttribute("type", "button");
    btn_up.setAttribute("id", 'up_' + r + (ls_index));
    btn_up.setAttribute("onclick", "up('" + (r + (ls_index)) + "')");
    btn_up.innerHTML = "&uarr;";

    var btn_del = document.createElement("button");
    btn_del.setAttribute("class", "btn btn-outline-danger");
    btn_del.setAttribute("type", "button");
    btn_del.setAttribute("id", 'del_' + r + (ls_index));
    btn_del.setAttribute("onclick", "del('" + r + (ls_index) + "')");
    btn_del.innerHTML = "X";

    div_group.appendChild(input)
    div_group_append.appendChild(btn_down)
    div_group_append.appendChild(btn_up)
    div_group_append.appendChild(btn_del)
    div_group.appendChild(div_group_append)

    li.appendChild(div_group)
    return li
}

function add_module(name, data, r, ls_index) {
    var new_r = r + (ls_index)

    var li = document.createElement("li");
    li.setAttribute("id", 'li_' + new_r);

    var input = document.createElement("input");
    input.value = name;
    input.setAttribute("name", new_r);
    input.setAttribute("id", 'input_' + new_r);
    input.setAttribute("class", "form-control border border-warning");
    input.setAttribute("type", "text");
    input.setAttribute("data-type", "module");
    input.setAttribute("placeholder", "Модуль");
    input.setAttribute("required", "");

    var div_group = document.createElement("div");
    div_group.setAttribute("class", "input-group mb-1");

    var div_group_append = document.createElement("div");
    div_group_append.setAttribute("class", "input-group-append");

    var btn_down = document.createElement("button");
    btn_down.setAttribute("class", "btn btn-outline-warning");
    btn_down.setAttribute("type", "button");
    btn_down.setAttribute("id", 'down_' + new_r);
    btn_down.setAttribute("onclick", "down('" + new_r + "')");
    btn_down.innerHTML = "&darr;";

    var btn_up = document.createElement("button");
    btn_up.setAttribute("class", "btn btn-outline-warning");
    btn_up.setAttribute("type", "button");
    btn_up.setAttribute("id", 'up_' + new_r);
    btn_up.setAttribute("onclick", "up('" + new_r + "')");
    btn_up.innerHTML = "&uarr;";

    var btn_del = document.createElement("button");
    btn_del.setAttribute("class", "btn btn-outline-danger");
    btn_del.setAttribute("type", "button");
    btn_del.setAttribute("id", 'del_' + new_r);
    btn_del.setAttribute("onclick", "del('" + new_r + "')");
    btn_del.innerHTML = "X";

    div_group.appendChild(input)
    div_group_append.appendChild(btn_down)
    div_group_append.appendChild(btn_up)
    div_group_append.appendChild(btn_del)
    div_group.appendChild(div_group_append)

    var ul = document.createElement("ul");
    ul.setAttribute("id", 'ul_' + new_r);

    setTimeout(function () {
        ls_index = 0
        for(var k in data[0]) {
            if (data[0][k][1] == 'module') {
                ul.appendChild(add_module(k, data[0][k], new_r + '.', ls_index));
            }
            else {
                ul.appendChild(add_lesson(k, data[0][k][0], new_r + '.', ls_index, data[0][k][0]));
            }
            ls_index++;
        }
    }, 100);
    li.appendChild(div_group)
    li.appendChild(ul)
    return li
}

function update_input_group(id, new_id) {
    input = document.getElementById('input_' + id);
    input.setAttribute("id", 'input_' + new_id);
    input.setAttribute("name", new_id);

    btn_down = document.getElementById('down_' + id);
    btn_down.setAttribute("id", 'down_' + new_id);
    btn_down.setAttribute("onclick", "down('" + new_id + "')");

    btn_up = document.getElementById('up_' + id);
    btn_up.setAttribute("id", 'up_' + new_id);
    btn_up.setAttribute("onclick", "up('" + new_id + "')");

    btn_del = document.getElementById('del_' + id);
    btn_del.setAttribute("id", 'del_' + new_id);
    btn_del.setAttribute("onclick", "del('" + new_id + "')");
}

function update_ul(id, new_id) {
    ul = document.getElementById('ul_' + id);
    if (ul) {
        ul.setAttribute("id", 'ul_' + new_id);

        var i = 0;
        while (true) {
            var li = document.getElementById('li_'+id+'.'+i);
            if (li) {
                li.setAttribute("id", 'li_' + new_id+'.'+i);
                update_input_group(id+'.'+i, new_id+'.'+i);
                update_ul(id+'.'+i, new_id+'.'+i);
                i++;
            }
            else {
                break
            }
        }
    }
}

function up(name) {
    mass_indexes = name.split('.');
    curr_index = parseInt(mass_indexes[mass_indexes.length - 1]);

    if (curr_index != 0) {
        previous_indexes = mass_indexes;
        previous_indexes[previous_indexes.length - 1] = parseInt(previous_indexes[previous_indexes.length - 1]) - 1
        previous_name = previous_indexes.join('.');

        update_ul(previous_name, name + '_');
        update_ul(name, previous_name);
        update_ul(name + '_', name);

        document.getElementById('li_' + previous_name).setAttribute("id", 'li_' + name + '_');
        document.getElementById('li_' + name).setAttribute("id", 'li_' + previous_name);
        document.getElementById('li_' + name + '_').setAttribute("id", 'li_' + name);

        update_input_group(previous_name, name + '_');
        update_input_group(name, previous_name);
        update_input_group(name + '_', name);

        element = document.getElementById('li_' + previous_name);
        element.parentNode.insertBefore(element, document.getElementById('li_' + name));
    }
    else {
        mass_indexes.pop();
        mass_indexes.pop();
        new_name = mass_indexes.join('.');

        var i = 0;
        while (true) {
            if (new_name != '') {
                li_id = new_name + '.' + i
            }
            else {
                li_id = i
            }

            li = document.getElementById('li_' + li_id);
            if (li) {
                i++;
            }
            else {
                break
            }
        }
        curr_li = document.getElementById('li_' + name);

        if (new_name == '') {
            curr_li.setAttribute("id", 'li_' + i);
            update_input_group(name, i);
            update_ul(name, i);
            document.getElementById('courses').appendChild(curr_li);
        }
        else {
            curr_li.setAttribute("id", 'li_' + new_name + '.' + i);
            update_input_group(name, new_name + '.' + i);
            update_ul(name, new_name + '.' + i);
            document.getElementById('ul_'+ new_name).appendChild(curr_li);
        }

        var i = 1;
        var host = name.split('.').slice(0, -1).join('.');
        while (true) {
            li = document.getElementById('li_' + host + '.' + i);
            if (li){
                li.setAttribute("id", 'li_' + host + '.' + (i-1));
                update_ul(host + '.' + i, host + '.' + (i-1));
                update_input_group(host + '.' + i, host + '.' + (i-1));
                i++;
            }
            else {
                break
            }
        }
    }
}

function down(name) {
    mass_indexes = name.split('.');
    curr_index = parseInt(mass_indexes[mass_indexes.length - 1]);

    next_indexes = mass_indexes;
    next_indexes[next_indexes.length - 1] = parseInt(next_indexes[next_indexes.length - 1]) + 1

    next_name = next_indexes.join('.');
    if (document.getElementById('li_' + next_name)) {
        up(next_name);
    }
}

function del(id) {
    li = document.getElementById('li_'+id);
    li.remove();

    mass_indexes = id.split('.');
    curr_index = parseInt(mass_indexes[mass_indexes.length - 1]);

    next_indexes = [...mass_indexes];
    while (true) {
        new_name = next_indexes.join('.') + '_';
        next_indexes[next_indexes.length - 1] = parseInt(next_indexes[next_indexes.length - 1]) + 1
        next_name = next_indexes.join('.');

        if (document.getElementById('li_' + next_name)) {
            document.getElementById('li_' + next_name).setAttribute("id", 'li_' + new_name);

            update_ul(next_name, new_name);

            update_input_group(next_name, new_name);
        }
        else {
            break;
        }
    }
    next_indexes = [...mass_indexes];
    while (true) {
        new_name = next_indexes.join('.');
        next_indexes[next_indexes.length - 1] = next_indexes[next_indexes.length - 1] + '_'
        next_name = next_indexes.join('.');

        if (document.getElementById('li_' + next_name)) {
            document.getElementById('li_' + next_name).setAttribute("id", 'li_' + new_name);

            update_ul(next_name, new_name);

            update_input_group(next_name, new_name);

            next_indexes[next_indexes.length - 1] = parseInt(next_indexes[next_indexes.length - 1]) + 1
        }
        else {
            break;
        }
    }
}