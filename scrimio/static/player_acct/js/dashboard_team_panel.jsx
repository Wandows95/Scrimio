
var DashboardTeamList = React.createClass({
	getInitialState: function(){
		// TeamList: Array of tuples with name and list of players
		return( { teamList:[{teamName:"MONO", playerList:[]}, {teamName:"NEWBEE", playerList:[]}, {teamName:"FNATIC", playerList:[]},
			{teamName:"VIOLET", playerList:[]}, {teamName:"TEAM IG", playerList:[]}], selectedIndex: 0 });
	},
	componentDidMount:function(){
		var data = ['teams':[], 'captain_of':[]];
		
		var exampleSocket = new WebSocket("ws://127.0.0.1:8000/scrimio/sockets/test/");
		
		$.ajax({
			type:'GET',
			url:this.props.getEndpoint,
			data: data,
			success: function(data){
				//this.setState(this.state.teamList.concat(data['teams']));
				//this.setState(this.state.teamLit.concat(data['captain_of']));
			}.bind(this)
		});
	},
	render:function(){
		var selectedTeam = this.state.teamList[this.state.selectedIndex];
		/* Left side of the panel */
		var teamPanels = this.state.teamList.map(function(team, index){
			return(
				<div className="row">
					<div className="columns small-5 callout panel dashboard-data-entry dashboard-team-entry-name">
						<p>{team.teamName}</p>
					</div>
					<div className="columns small-7 callout panel dashboard-data-entry dashboard-team-entry-player">
						<div className="row">
							<div className="columns small-10">
								<p>Player {index}</p>
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

var reactEntry = document.getElementById('react-dashboard-team-list');

ReactDOM.render(
  <DashboardTeamList getEndpoint={reactEntry.getAttribute('data-get-endpoint')}/>,
  reactEntry
);