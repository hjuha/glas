$( function() {
    var id = 1;
    var option_ids = {};
    $( ".slider" ).slider({ min: 0, max: 100, value: 50 });
    $( ".mc_input" ).checkboxradio();
    $( ".jbtn" ).button();
    $("#new_slider").click(function(){
        $("#questions").append(`<fieldset id="field${id}"><span id="delete${id}" class="delete">X</span><table>
            <tr><td>Question:</td><td><input name="question${id}" type="text"></td>
            <tr><td>Left value:</td><td><input name="left${id}" type="text"></td>
            <tr><td>Right value:</td><td><input name="right${id}" type="text"></td>
            </table></fieldset>`);
        let target_field = `#field${id}`;
        $(`#delete${id}`).click(function() {
            $(target_field).remove();
        });
        id += 1;
    });
    $(".color_picker").spectrum({
        color: "#ff0000",
        preferredFormat: "rgb"
    });
    $("#new_multichoice").click(function(){
        option_ids[id] = 1;
        $("#questions").append(`<fieldset id="field${id}"><span id="delete${id}" class="delete">X</span>Question: <input name="question${id}" type="text"><br>
            Options:<br>
            <div id="options${id}">
            <div id="option${id}_${option_ids[id]}"><input type="text" name="option${id}_${option_ids[id]}"><span id="delete${id}_${option_ids[id]}" class="delete_choice">X</span><br></div>
            </div>
            <button type="button" class="jbtn ui-button ui-widget ui-state-default ui-corner-all" id="new_option${id}">Add option</button>
            </fieldset>`);
        let target_option = `#option${id}_${option_ids[id]}`
        $(`#delete${id}_${option_ids[id]}`).click(function() {
            $(target_option).remove();
        });
        let my_id = id;
        let target_field = `#field${id}`;
        $(`#delete${id}`).click(function() {
            $(target_field).remove();
        });
        $(`#new_option${id}`).click(function(){
            option_ids[my_id]++; $("#options" + my_id).append(`<div id="option` + my_id + `_${option_ids[my_id]}"><input type="text" name="option` + my_id + `_${option_ids[my_id]}"><span id="delete` + my_id + `_${option_ids[my_id]}" class="delete_choice">X</span><br></div>`);
            let target_option = `#option` + my_id + `_${option_ids[my_id]}`;
            $(`#delete` + my_id + `_${option_ids[my_id]}`).click(function() {
                $(target_option).remove();
            });
        });
        id += 1;
    });
    $("#new_multichoice_multi").click(function(){
        option_ids[id] = 1;
        $("#questions").append(`<fieldset id="field${id}"><span id="delete${id}" class="delete">X</span>Question: <input name="question${id}" type="text"><br>
            Maximum number of choices:<br>
            <input name="maximum${id}" type="text"><br>
            Options:<br>
            <div id="options${id}">
            <div id="option${id}_${option_ids[id]}"><input type="text" name="option${id}_${option_ids[id]}"><span id="delete${id}_${option_ids[id]}" class="delete_choice">X</span><br></div>
            </div>
            <button type="button" class="jbtn ui-button ui-widget ui-state-default ui-corner-all" id="new_option${id}">Add option</button>
            </fieldset>`);
        let target_option = `#option${id}_${option_ids[id]}`
        $(`#delete${id}_${option_ids[id]}`).click(function() {
            $(target_option).remove();
        });
        let my_id = id;
        let target_field = `#field${id}`;
        $(`#delete${id}`).click(function() {
            $(target_field).remove();
        });
        $(`#new_option${id}`).click(function(){
            option_ids[my_id]++; $("#options" + my_id).append(`<div id="option` + my_id + `_${option_ids[my_id]}"><input type="text" name="option` + my_id + `_${option_ids[my_id]}"><span id="delete` + my_id + `_${option_ids[my_id]}" class="delete_choice">X</span><br></div>`);
            let target_option = `#option` + my_id + `_${option_ids[my_id]}`;
            $(`#delete` + my_id + `_${option_ids[my_id]}`).click(function() {
                $(target_option).remove();
            });
        });
        id += 1;
    });
    $("#result_form").submit(function(){
        let sliders = document.getElementsByClassName("slider");
        for (let slider of sliders) {
            $("#result_form").append(`<input style="display: none;" type="text" name="${slider.id}" value="${$(slider).slider("value")}">`);
        }
        return true;
    });
});