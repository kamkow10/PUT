import React from 'react';
import ReactDOM from 'react-dom';

class AddTask extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            text: ""
        }
        this.onButtonAddClick = this.onButtonAddClick.bind(this)
        this.onTextFieldChange = this.onTextFieldChange.bind(this)
        document.addEventListener("keyup", function(event) {
            event.preventDefault();
            if (event.keyCode === 13) {
                document.getElementById('addButton').click()
            }
        })
    }
    
    onTextFieldChange(event) {
        this.setState({
            text: event.target.value
        })
    }
    
    onButtonAddClick() {
        document.getElementById("textfield").value = ""
        this.props.addTask(this.state.text)
        document.getElementById("textfield").focus()
    }
    
    render() {
        return (
            <div>
                <input id="textfield" type="text" onChange={this.onTextFieldChange} />
                <button id="addButton" onClick={this.onButtonAddClick}>Add</button>
            </div>
        )
    }
}

export default AddTask
