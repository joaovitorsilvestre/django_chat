angular.module('index').service('chatApi', function($http, $httpParamSerializerJQLike){
	this.users_on = function(){
		return (
			$http({
				url: '/chat/users_on/',
				method: 'GET'
			})
		)
	}
	this.get_messages = function(user){
		return(
			$http({
				url: '/chat/messages_get/' + user,
				method: 'GET'
			})
		)
	}
	this.send_messages = function(text, toUser){
		return(
			$http({
				url: '/chat/messages_send/',
				method: 'POST',
				data: $httpParamSerializerJQLike({
					toUser: toUser,
					text:text
				}),
				headers: {'Content-Type': 'application/x-www-form-urlencoded'},	
			})
		)
	}
})