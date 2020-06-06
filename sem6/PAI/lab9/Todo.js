import React from 'react';
import ReactDOM from 'react-dom';

import Task from "./Task"

class Todo extends React.Component {
    constructor(props) {
        super(props)
        this.onTaskChange = this.onTaskChange.bind(this)
    }

    onTaskChange(key, value) {
        this.props.onTasksChange(key, value)
    }

    render() {
        let count = 0
        let tasks = this.props.tasks.map(task => {
            if (!(this.props.hide && task.value)) {
                count++
                return (
                    <Task key={task.key} id={task.key} text={task.text} onTaskChange={this.onTaskChange} checked={task.value} />
                )
            }
        })

        return (
            <div>
                {count > 0 ?
                    tasks : <p>Nothing to do</p>
                }
            </div>
        )
    }
}

export default Todo
