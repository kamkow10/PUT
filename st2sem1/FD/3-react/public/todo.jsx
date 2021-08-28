class Todo extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            todos: [],
            todosToShow: [],
            text: '',
            selectedOption: 'ALL'
        }
        this.getTodos();
    }

    render() {
        return (
            <div>
                <div className="jumbotron text-center">
                    <h1>nodeTODO: <span className="label label-info">{this.state.todos.length}</span></h1>
                </div>
                <div id="radios" className="radios">
                    <label>
                        <input
                            type="radio"
                            value="ALL"
                            checked={this.state.selectedOption === "ALL"}
                            onChange={(e) => this.onRadioChanged(e)}
                        />
                        ALL
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="TODO"
                            checked={this.state.selectedOption === "TODO"}
                            onChange={(e) => this.onRadioChanged(e)}
                        />
                        TODO
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="DONE"
                            checked={this.state.selectedOption === "DONE"}
                            onChange={(e) => this.onRadioChanged(e)}
                        />
                        DONE
                    </label>
                </div>

                <div id="todo-list" className="row">
                    <div className="col-sm-8 col-sm-offset-2">
                        {this.state.todosToShow.map((todo => {
                            return (
                                <div className="checkbox" key={todo._id}>
                                    <label>
                                        <input type="checkbox" onChange={() => this.updateTodo(todo)}
                                               checked={todo.done}/>
                                        {todo.text}
                                    </label>
                                    <button className="btn btn-secondary btn-lg" type="button"
                                            onClick={() => this.deleteTodo(todo._id)}>Usuń
                                    </button>
                                </div>
                            )
                        }))}
                    </div>
                </div>

                <div id="todo-form" className="row">
                    <div className="col-sm-8 col-sm-offset-2 text-center">
                        <form>
                            <div className="form-group">
                                <input id="newTodo" type="text" className="form-control input-lg text-center"
                                       placeholder="co jeszcze chcesz zrobić?" value={this.state.text}
                                       onChange={this.onInputChange}/>
                            </div>
                            <button type="button" className="btn btn-primary btn-lg"
                                    onClick={() => this.createTodo()}>Dodaj
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        )
    }

    getTodos() {
        fetch('http://localhost:4000/api/todos')
            .then(response => response.json())
            .then(data => this.setState({todos: data, todosToShow: data}));
    }

    updateTodo(todo) {
        todo.done = !todo.done;
        const requestOptions = {
            method: 'PATCH',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(todo)
        };
        fetch('http://localhost:4000/api/todos', requestOptions)
            .then(response => response.json())
            .then(data => this.setState(
                {
                    todos: data,
                    todosToShow: this.getTodosToShow(this.state.selectedOption, data)
                }
            ));
    }

    deleteTodo(id) {
        const requestOptions = {
            method: 'DELETE'
        }
        fetch('http://localhost:4000/api/todos/' + id, requestOptions)
            .then(response => response.json())
            .then(data => this.setState(
                {
                    todos: data,
                    todosToShow: this.getTodosToShow(this.state.selectedOption, data)
                }
            ));
    }

    createTodo() {
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: this.state.text})
        }
        fetch('http://localhost:4000/api/todos/', requestOptions)
            .then(response => response.json())
            .then(data => this.setState(
                {
                    todos: data,
                    text: '',
                    todosToShow: this.getTodosToShow(this.state.selectedOption, data)
                }
            ));
    }

    onRadioChanged(e) {
        this.setState({
            selectedOption: e.target.value,
            todosToShow: this.getTodosToShow(e.target.value, this.state.todos)
        });
    }

    getTodosToShow(option, todos) {
        let todosElementsList = [];
        for (let todo of todos) {
            switch (option) {
                case 'DONE':
                    todosElementsList = todos.filter((todo) => {
                        return todo.done
                    });
                    break;
                case 'TODO':
                    todosElementsList = todos.filter((todo) => {
                        return !todo.done
                    });
                    break;
                case 'ALL':
                    todosElementsList = todos;
                    break;
            }
        }
        return todosElementsList;
    }

    onInputChange = (e) => {
        this.setState({text: e.target.value})
    }
}


ReactDOM.render(
    <Todo/>,
    document.getElementById('todo')
);
