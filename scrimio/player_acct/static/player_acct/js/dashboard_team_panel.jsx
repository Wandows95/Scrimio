var TeamPlayerList = React.createClass({
	getInitialState:function() {
		return({playerStatusList:[]})
	},
	componentDidMount:function(){
	},
	render:function(){
		
		this.props.teamSocket.onmessage = function(event) {
			/*var data = JSON.parse(event.data)
			console.log(data)
			if(data['action'] == "team-queue-player-update")
			{
				// Preserve previous status list
				var currentStatusList = this.state.playerStatusList;
				currentStatusList[data['username']] = data['status']
				this.setState({playerStatusList:currentStatusList})
				console.log(this.state.playerStatusList[data['username']])
			}*/
		}.bind(this)
	
		var sendSocketUpdate = function(){
			var message = {
				message: "placeholder"
			};

			this.props.teamSocket.send(JSON.stringify(message));
		}.bind(this)

		var playerList = this.props.playerList.map(function(playerTuple){
			var readyButton;
			var statusCircle;

			if(this.props.localUsername == playerTuple['username'])
				readyButton = <button onClick={sendSocketUpdate} className="dashboard-team-player-ready-button">Ready</button>

			if(playerTuple['status']['state'] == 1)
				statusCircle = <div className="circle color-online"></div>
			else if(playerTuple['status']['state'] == 2 && playerTuple['status']['current_team'] === this.props.teamName)
				statusCircle = <div className="circle color-ready"></div>
			else
				statusCircle = <div className="circle color-offline"></div>

			/*
			if(this.state.playerStatusList.hasOwnProperty(playerTuple['username'])){
				if(this.state.playerStatusList[playerTuple['username']] == 1)
					statusCircle = <div className="circle color-online"></div>
				else if(this.state.playerStatusList[playerTuple['username']] == 2 && this.state.playerStatusList[playerTuple['username']] === this.props.teamName)
					statusCircle = <div className="circle color-ready"></div>
				else
					statusCircle = <div className="circle color-offline"></div>
			}*/

			return(
			<div className="row dashboard-team-player-entry-row">
				<div className="small-0 medium-2 columns"></div>
				<div className="small-10 medium-5 columns dashboard-team-player-entry-name-container">
					<p className="dashboard-team-player-entry-name">{playerTuple['username']}</p>
				</div>
				<div className="small-0 medium-2 columns">{readyButton}</div>
				<div className="small-2 medium-1 columns dashboard-team-player-entry-status-container">
					{statusCircle}
				</div>
				<div className="small-0 medium-2 columns"></div>
			</div>
			);
		}, this);

		return(<div className="row dashboard-player-list-container">{playerList}</div>);
	}
});

var TeamEntry = React.createClass({
	render:function(){
		return (
			<div className="row">
				<div className="row team-entry-row">
					<div className="small-0 medium-2 columns"></div>
					<div className="small-10 medium-5 columns team-entry-name">
						<button className="dashboard-team-select-button expand-button">{this.props.teamName}</button>
					</div>
					<div className="small-0 medium-2 columns"></div>
					<div className="small-2 medium-1 columns team-entry-elo">
						<h3>{this.props.teamElo}</h3>
					</div>
					<div className="small-0 medium-2 columns"></div>
				</div>
				<TeamPlayerList teamName={this.props.teamName} teamSocket={this.props.teamSocket} localUsername={this.props.localUsername} playerList={this.props.teamPlayers} />
			</div>
		);
	}
});

var PlayerTeamList = React.createClass({
	getInitialState: function(){
		var self = this;
		this.teamSockets = new Array();
		var newTeamList = [];
		var newCaptainList = [];

		$.ajax({
	        url: self.props.endpoint,
	        dataType:"JSON",
	        type: "GET",
	        success:function(data){
				newTeamList = data.teams;
				newCaptainList = data.captain_of;

				newCaptainList.map(function(team){
					self.teamSockets[team['name']] = new WebSocket("ws://127.0.0.1:8000/dota/sockets/status/" + team['name'] + "/");
					console.log(self.teamSockets[team['name']]);
				});

				newTeamList.map(function(team){
					self.teamSockets[team['name']] = new WebSocket("ws://127.0.0.1:8000/dota/sockets/status/" + team['name'] + "/");
					console.log(self.teamSockets[team['name']]);
				});
			}
    	});

    	return ({teamList: newTeamList, captainList: newCaptainList})
	},
	componentDidMount:function(){
		var self = this;
		

		setInterval(function(){
			$.ajax({
		        url: self.props.endpoint,
		        dataType:"JSON",
		        type: "GET",
		        success:function(data){
					self.setState({teamList: data.teams});
					self.setState({captainList: data.captain_of});
				}
	    	});
		}.bind(this), 5000);
	},
	render: function(){
		var teamList = this.state.teamList.map(function(team){
			var teamPlayers = new Array();
			teamPlayers = teamPlayers.concat(team['players']);
			teamPlayers = teamPlayers.concat(team['captain']);
			console.log(teamPlayers);
			console.log(team['captain']);
			return <TeamEntry teamSocket={this.teamSockets[team.name]} teamName={team.name} localUsername={this.props.localUsername} teamElo={team.elo} teamPlayers={teamPlayers} />
		}, this);

		var captainList = this.state.captainList.map(function(team){
			var teamPlayers = new Array();
			teamPlayers = teamPlayers.concat(team['players']);
			teamPlayers = teamPlayers.concat(team['captain']);
			
			return <TeamEntry teamSocket={this.teamSockets[team.name]} teamName={team.name} localUsername={this.props.localUsername} teamElo={team.elo} teamPlayers={teamPlayers} />
		}, this);

		return(
			<div className="row player-team-list">
				<div className="row player-team-list-header">
					<div className="medium-2 small-0 columns"></div>
					<div className="small-10 medium-7 columns team-entry-header-name">
						<h2 className="react_team_list_team_header">Name</h2>
					</div>
					<div className="small-2 medium-1 columns team-entry-header-elo">
						<h2 className="react_team_list_elo_header">Elo</h2>
					</div>
					<div className="medium-2 small-0 columns"></div>
				</div>
				{captainList}
				{teamList}
			</div>
		);
	}
});

var reactEntry = document.getElementById('react-team-view');

ReactDOM.render(
  <PlayerTeamList localUsername={reactEntry.getAttribute('data-local-username')} endpoint={reactEntry.getAttribute('data-endpoint')} />,
  document.getElementById('react-team-view')
);