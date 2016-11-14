var DashboardTeamEntryRow = React.createClass({
	render: function(){
		return(
			<div className="row">
				<div className="columns small-5 callout panel dashboard-data-entry dashboard-team-entry-name">
					<p>{this.props.teamName}</p>
				</div>
				<div className="columns small-7 callout panel dashboard-data-entry dashboard-team-entry-player">
					<div className="row">
						<div className="columns small-10">
							<p>{this.props.playerName}</p>
						</div>
						<div className="columns small-2">
							<div className="dashboard-player-status player-online"></div>
						</div>
					</div>
				</div>
			</div>
		);
	}
});

var DashboardTeamList = React.createClass({
	getInitialState: function(){
		// TeamList: Array of tuples with name and list of players
		return( { teamList:[], selectedIndex: 0 });
	},
	componentDidMount:function(){
		var data = ['teams':[], 'captain_of':[]];
		
		$.ajax({
			type:'GET',
			url:this.props.getEndpoint,
			data: data,
			success: function(data){
				if(data['teams'] != undefined)
					this.setState(this.state.teamList.concat(data['teams']));
				if(data['captain_of'] != undefined)
					this.setState(this.state.teamList.concat(data['captain_of']));
			}.bind(this)
		});
	},
	render:function(){
		var selectedTeam = this.state.teamList[this.state.selectedIndex];
		var teamList = this.state.teamList;
		var panelRows = [];

		for(var i = 0; i < 5; i++){
			var teamName = (teamList != undefined && teamList.length-1 >= i) ? teamList[i]["name"] : " "; // Test if this is a team row or a blank
			var playerName = (selectedTeam != undefined && selectedTeam["players"].length-1 >= i) ? selectedTeam["players"]["username"] : " ";

			panelRows.push(<DashboardTeamEntryRow teamName={teamName} playerName={playerName}/>)
		}

		return(
			<div className="row dashboard-team-entry">
				{panelRows}
			</div>
		);
	}
});

var reactEntry = document.getElementById('react-dashboard-team-list');

ReactDOM.render(
  <DashboardTeamList getEndpoint={reactEntry.getAttribute('data-get-endpoint')}/>,
  reactEntry
);