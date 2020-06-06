import React from 'react';
import ReactDOM from 'react-dom';

class Filter extends React.Component {
    constructor(props) {
        super(props)
        this.onCheckboxChange = this.onCheckboxChange.bind(this)
    }

    onCheckboxChange(event) {
        this.props.manageTasks(event.target.checked)
    }
    
    render() {
        return (
            <div>
                <input type="checkbox" onChange={this.onCheckboxChange}/> Hide complited
            </div>
        )
    }
}

export default Filter
