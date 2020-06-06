import React from 'react';
import ReactDOM from 'react-dom';

class Task extends React.Component {
    constructor(props) {
        super(props)
        this.onTaskChange = this.onTaskChange.bind(this)
    }

    onTaskChange(event) {
        console.log(event.target.checked)
        this.props.onTaskChange(this.props.id, event.target.checked)
    }
    
    render() {
        return (
            <div>
                <input type="checkbox" checked={this.props.checked} onChange={this.onTaskChange}/> {this.props.text}
            </div>
        )
    }
}

export default Task
