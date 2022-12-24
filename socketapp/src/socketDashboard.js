import React from "react";
import io from 'socket.io-client';
import search_page from "./searchPage";
import SearchField from "./SearchField"

class Dashboard extends React.Component {
    state = {
        socketData: "",
    }

    componentWillUnmount() {
        this.socket.close()
        console.log("component unmounted")
    }
    componentDidMount() {
        var sensorEndpoint = "http://localhost:5015"
            this.socket = io.connect(sensorEndpoint, {
            reconnection: true,
            transports: ['websocket']
        });
        console.log("component mounted")
            this.socket.on("responseMessage", message => {
                this.setState({'socketData': message.data})
                
                console.log("responseMessage", message)
            })
       
    }
    
    handleEmit=()=>{      
        this.socket.emit("message", {'data':'Send data'})

    }

    handleSearch = (value) => {
        this.socket.emit("search", { 'data': value })

    }

    render() {
        return (
            <div>
            <SearchField placeholder="Search candidates" onChange={this.handleSearch}/>
            {search_page(this.handleEmit, this.state.socketData)}
            </div>
        )
    }
}
export default Dashboard;