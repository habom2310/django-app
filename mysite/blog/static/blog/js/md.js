var myCodeMirror;
var requestSend = false;
var isSending = false;

function ajaxUpdatePreview() {
    requestSend = true;
    tryAjaxUpdatePreview();
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function tryAjaxUpdatePreview() {
    if(!isSending && requestSend) {
        requestSend = false;
        isSending = true;
        var mdtext = $("#markdown_input").val()
        // console.log(mdtext);

        $.ajax({
            type: "POST",
            url: "/blog/ajax/preview/",
            headers: { "X-CSRFToken":  csrftoken },
            data: {
                "mdtext": JSON.stringify(mdtext)
            },
            dataType: "json",
            // contentType: "text/plain",
            success: function( data ) {
                console.log("success");
                console.log(data["html_output"]);
                isSending = false;
                setTimeout(tryAjaxUpdatePreview, 0);
                $("#html_result").html(data["html_output"]);
            },
            error: function() {
                alert('Error occured');
            }
    });
    }
}


function updateMarkdownInput(value) {
    myCodeMirror.setValue(value);
}

$(document).ready(function() {

    // Setup custom header height
    head_height = $('#head').outerHeight(true);
    $('#mdedit').css('top', head_height+'px');
    $('#mdedit-body').css('top', (head_height+$('#mdedit').height())+'px');
    $('#markdown_input').bind('input propertychange', function(){
        console.log(this.value);
        ajaxUpdatePreview();
    });
    // Setup CodeMirror for markdown input
    // CodeMirror.commands.save = function(instance) {ajaxSaveFile();}

    // myCodeMirror = CodeMirror.fromTextArea(document.getElementById('markdown_input'), {
    //     value: "",
    //     mode: {name:"markdown",fencedCodeBlocks:true, underscoresBreakWords:false},
    //     indentUnit: "4",
    //     showCursorWhenSelecting: true,
    //     theme: "neat",
    //     vimMode: false
    //     });
    // $(".CodeMirror").addClass("form-control");
    // $(".CodeMirror").addClass("focusedInput");
    // $(".CodeMirror").attr('form', 'editform');
    // myCodeMirror.setSize("100%","100%");
    // myCodeMirror.on("change", function(instance, changeObj) {ajaxUpdatePreview();});

    // Setup scrollbars sync
    // var s1 = myCodeMirror.display.scrollbars.vert
    // var s1 = $('#markdown_input').get(0).scrollTop;
    // var s2 = $('#html_result')[0]

    // function select_scroll(e) {
    //     viewHeight = s2.getBoundingClientRect().height
    //     ratio = (s2.scrollHeight-viewHeight)/(s1.scrollHeight-viewHeight)
    //     s2.scrollTop = s1.scrollTop*ratio;
    // }

    // s1.addEventListener('scroll', select_scroll, false);

    // Set Focus on markdown input
    // $('#pleaseWaitDialog').on('hidden.bs.modal', function () {myCodeMirror.focus()})

    ajaxUpdatePreview();

});