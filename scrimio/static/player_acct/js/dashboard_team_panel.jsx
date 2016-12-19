var TeamPlayerList = React.createClass({
	render:function(){
		var playerList = this.props.playerList.map(function(playerTuple){
			return(
			<div className="row dashboard-team-player-entry-row">
				<div className="small-0 medium-2 columns"></div>
				<div className="small-10 medium-5 columns dashboard-team-player-entry-name-container">
					<p className="dashboard-team-player-entry-name">{playerTuple['username']}</p>
				</div>
				<div className="small-0 medium-2 columns"></div>
				<div className="small-2 medium-1 columns team-entry-elo">
					<p>{playerTuple['status']['state']}</p>
				</div>
				<div className="small-0 medium-2 columns"></div>
			</div>
			);
		});

		return(<div className="row">{playerList}</div>);
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
				<TeamPlayerList playerList={this.props.teamPlayers} />
			</div>
		);
	}
});

var PlayerTeamList = React.createClass({
	getInitialState: function(){
		return({teamList:[], captainList: []});
	},
	componentDidMount:function(){
		$.ajax({
			dataType:"JSON",
			url: this.props.endpoint,
			success:function(data){
				this.setState({teamList: data.teams});
				this.setState({captainList: data.captain_of});
			}.bind(this)
		});
	},
	render: function(){
		var teamList = this.state.teamList.map(function(team){
			var teamPlayers = new Array();
			teamPlayers = teamPlayers.concat(team['players']);
			teamPlayers = teamPlayers.concat(team['captain']);
			console.log(teamPlayers);
			console.log(team['captain']);
			return <TeamEntry teamName={team.name} teamElo={team.elo} teamPlayers={teamPlayers} />
		});

		var captainList = this.state.captainList.map(function(team){
			var teamPlayers = new Array();
			teamPlayers = teamPlayers.concat(team['players']);
			teamPlayers = teamPlayers.concat(team['captain']);
			console.log(teamPlayers);
			
			return <TeamEntry teamName={team.name} teamElo={team.elo} teamPlayers={teamPlayers} />
		});

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
  <PlayerTeamList endpoint={reactEntry.getAttribute('data-endpoint')} />,
  document.getElementById('react-team-view')
);