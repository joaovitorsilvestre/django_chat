function get_users_on(){
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url:'/chat/users_on',
        success: function(data){
            console.log(data)
            refresh_users(data)
        }
    })
}

var selected_user = 'null'
function refresh_users(data){
    var box_users = document.getElementById('box_users');
    $("#box_users").html("");
    
    for (i=0; i<data.length; i++){
        var obj = document.createElement('div');
        obj.className = 'box_user_unique';
        obj.name = data[i]
            
        var t = document.createTextNode(data[i]);
        obj.appendChild(t);
        obj.addEventListener('click', function(){
            var divs = document.getElementsByClassName('box_user_unique');
            for (i=0; i<divs.length; i++ ){
                divs[i].style.backgroundColor = 'cadetblue'
            }
            this.style.backgroundColor = 'blue'
            selected_user = this.name
        });
        document.getElementById('box_users').appendChild(obj);
        console.log(obj);
    }
}

$(document).on('submit','#form_message', function(e){
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url:'/chat/send_message',
            data: {
                de: $('#usuario').val(),
                para: selected_user,
                message: $('#text_input').val()
            },
            success: function(resposta){
                refresh_chat()
            }
        })
    });

function refresh_chat(){
    $.ajax({
        type: 'POST',
        url: '/chat/get_message',
        data: {
            de: $('#usuario').val(),
            para: selected_user
        },
        success: function(resposta){
            display_chat(resposta);
        }
    })
    
    console.log('chat atualizado');
}

function display_chat(msgs_lista){
    $('#box_messages').html('')
    
    for (i=0; i< msgs_lista.length; i++){
        //verificar o nome na string
        user = document.getElementById('usuario').value        
        
        if (msgs_lista[i].indexOf(user) > -1){
            var obj = document.createElement('div');
            obj.className = 'msg_unique_user';        
            var t = document.createTextNode(msgs_lista[i]);
            obj.appendChild(t);
            document.getElementById('box_messages').appendChild(obj)
        }else{
            var obj = document.createElement('div');
            obj.className = 'msg_unique_other';        
            var t = document.createTextNode(msgs_lista[i]);
            obj.appendChild(t);
            document.getElementById('box_messages').appendChild(obj)      
        }            
    }   
}


