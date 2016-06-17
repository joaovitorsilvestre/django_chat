angular.module('index').controller('indexCtrl', function($scope, $interval, chatApi){
	var update_users = function(){
		chatApi.users_on().success(function(response){
			$scope.users = response
			console.log(response)
		})
	}

	var update_messages = function(){
		chatApi.get_messages($scope.user_selected).success(function(response){
			console.log(response)
			$scope.messages = response
		})
	}

	$scope.class_message = function(message){
		if (message.indexOf($scope.user_selected)){       //esta função verifica quem é o dono da menssagem e retorna o nome da classe certa
			lol = 'msg_unique_user'
		}else{
			lol = 'msg_unique_other'
		}
		return lol
	}

	$scope.send_message = function(message){
		console.log('enviando menssagem para ', $scope.user_selected)
		chatApi.send_messages(message, $scope.user_selected).success(function(response){
			console.log(response)
			update_messages()
		})
	}

	$scope.select_user = function(user){
		$scope.user_selected = user
		$scope.messages = []
		console.log(user)
		//update_messages()
		$interval(update_messages, 2000) // BUG, quando troca de usuario o interval continual fazendo requisição dos dados, e cada vez mais rapido
	}

	update_users()

})
