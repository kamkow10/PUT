import React, {useDebugValue} from 'react';
import ReactDOM from 'react-dom';

import Filter from "./Filter"
import AddTask from "./AddTask"
import Todo from "./Todo"

class App extends React.Component {
    constructor() {
        super()
        this.state = {
            tasks: [],
            hide: false
        }
        this.key = 0
        this.addTask = this.addTask.bind(this)
        this.onTaskChange = this.onTaskChange.bind(this)
        this.manageTasks = this.manageTasks.bind(this)
    }
    
    addTask(text) {
        this.key++
        this.setState(prevState => {
            let newTasks = prevState.tasks
            newTasks.push({key: this.key, text: text, value: false})
            return {
                tasks: newTasks
            }
        })
    }

    manageTasks(hide) {
        this.setState(prevState => {
            return {
                tasks: prevState.tasks,
                hide: hide
            }
        }
       )
    }

    onTaskChange(key, value) {
        this.setState(prevState => {
            let foundIndex = prevState.tasks.findIndex(x => x.key === key)
            let updatedTask = {key: key, text: prevState.tasks[foundIndex].text, value: value}
            let newState = prevState
            newState.tasks[foundIndex] = updatedTask
            return newState
        })
    }
    
    render() {
        return (
            <div>
                <Filter manageTasks={this.manageTasks} />
                <hr/>
                <Todo tasks={this.state.tasks} onTasksChange={this.onTaskChange} hide={this.state.hide} />
                <hr/>
                <AddTask addTask={this.addTask} />
            </div>
        )
    }
}

export default App
