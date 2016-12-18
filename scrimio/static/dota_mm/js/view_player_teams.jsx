var TeamEntry = React.createClass({
	render:function(){
		return (
			<div is class="row team-entry-row">
				<div is class="small-6 medium-8 columns team-entry-name">
					<h3>{this.props.teamName}</h3>
				</div>
				<div is class="small-6 medium-4 columns team-entry-elo">
					<h3>{this.props.teamElo}</h3>
				</div>
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
			return <TeamEntry teamName={team.name} teamElo={team.elo} />
		});

		var captainList = this.state.captainList.map(function(team){
			console.log(team);
			return <TeamEntry teamName={team.name} teamElo={team.elo} />
		});

		return(
			<div className="row player-team-list">
				<div className="row player-team-list-header">
					<div className="small-6 medium-8 columns team-entry-header-name">
						<h2 className="react_team_list_team_header">Name</h2>
					</div>
					<div className="small-6 medium-4 columns team-entry-header-elo">
						<h2 className="react_team_list_elo_header">Elo</h2>
					</div>
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