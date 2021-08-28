var nodeTodo = angular.module("nodeTodo", []).config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.patch = {
        'Content-Type': 'application/json;charset=utf-8'
    }
}]);

function mainController($scope, $http) {
  $scope.formData = {};
  $scope.todos = [];
  $scope.todosToShow = [];
  $scope.showOptions = 'TODO';

  // when landing on the page, get all todos and show them
  $http
    .get("http://localhost:4000/api/todos")
    .success(function(data) {
      $scope.todos = data;
        showTodos();

    })
    .error(function(data) {
      console.log("Error: " + data);
    });

  // when submitting the add form, send the text to the node API
  $scope.createTodo = function() {
    $http
      .post("http://localhost:4000/api/todos", $scope.formData)
      .success(function(data) {
        document.getElementById("newTodo").value = "";
        $scope.todos = data;
        showTodos();
      })
      .error(function(data) {
        console.log("Error: " + data);
      });
  };

  // update a todo after checking it
  $scope.updateTodo = function(todo) {
      console.log(todo);
      $http({ method: 'PATCH', url: 'http://localhost:4000/api/todos', data: todo})
        .success(function(data) {
          $scope.todos = data;
            showTodos();
        })
        .error(function(data) {
          console.log("Error: " + data);
        });
  };

  // delete a todo after checking it
  $scope.deleteTodo = function(id) {
    $http
      .delete("http://localhost:4000/api/todos/" + id)
      .success(function(data) {
        $scope.todos = data;
          showTodos();
      })
      .error(function(data) {
        console.log("Error: " + data);
      });
  };

  const showTodos = () => {
      if ($scope.showOptions === 'ALL') {
          $scope.todosToShow = $scope.todos;
      } else if ($scope.showOptions === 'TODO') {
          $scope.todosToShow = $scope.todos.filter((todo) => { return !todo.done });
      } else if ($scope.showOptions === 'DONE') {
          $scope.todosToShow = $scope.todos.filter((todo) => { return todo.done });
      }
      $scope.$apply();
  }

  document.getElementById('radios').addEventListener('click', () => { showTodos(); })
}
