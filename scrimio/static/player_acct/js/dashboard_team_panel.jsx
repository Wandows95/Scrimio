/*var DashboardTeamPanel = React.createClass({
	getInitialState: function(){
		return({teamName:"", players:[{username:"Arteezy", isOnline: true}, {username:"FEAR", isOnline: false}]});
	},
	mouseOver: function(){
        this.setState({hover: true});
    },

    mouseOut: function(){
        this.setState({hover: false});
    },
});*/

var DashboardTeamList = React.createClass({
	getInitialState: function(){
		// TeamList: Array of tuples with name and list of players
		return( { teamList:[{teamName:"MONO", playerList:[]}, {teamName:"NEWBEE", playerList:[]}, {teamName:"FNATIC", playerList:[]},
			{teamName:"VIOLET", playerList:[]}, {teamName:"TEAM IG", playerList:[]}], selectedIndex: 0 });
	},
	render:function(){
		console.log(this.state.teamList);
		var selectedTeam = this.state.teamList[this.state.selectedIndex];
		/* Left side of the panel */
		var teamPanels = this.state.teamList.map(function(team){
			return(
				<div className="row">
					<div className="columns small-5 callout panel dashboard-data-entry dashboard-team-entry-name">
						<p>{team.teamName}</p>
					</div>
					<div className="columns small-7 callout panel dashboard-data-entry dashboard-team-entry-player">
						<div className="row">
							<div className="columns small-10">
								<p>Player P</p>
							</div>
							<div className="columns small-2">
								<div className="dashboard-player-status player-online"></div>
							</div>
						</div>
					</div>
				</div>
			);
		});

		return(
			<div className="row dashboard-team-entry">
				{teamPanels}
			</div>
		);
	}
});

ReactDOM.render(
  <DashboardTeamList />,
  document.getElementById('react-dashboard-team-list')
);