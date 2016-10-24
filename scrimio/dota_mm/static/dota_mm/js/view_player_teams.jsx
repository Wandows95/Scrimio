var TeamEntry = React.createClass({
	render:function(){
		return (
			<div className="row team-entry-row">
				<div className="small-6 medium-8 columns team-entry-name">
					<h3>{this.props.teamName}</h3>
				</div>
				<div className="small-6 medium-4 columns team-entry-elo">
					<p>{this.props.teamElo}</p>
				</div>
			</div>
		);
	}
});

var PlayerTeamList = React.createClass({
	getInitialState: function(){
		return({teamList:[]});
	},
	componentDidMount:function(){
		$.ajax({
			dataType:"JSON",
			url: this.props.endpoint,
			success:function(data){
				this.setState({teamList: data.teams});
			}.bind(this)
		});
	},
	render: function(){
		var teamList = this.state.teamList.map(function(team){
			return <TeamEntry teamName={team.name} teamElo={team.elo} />
		});

		return(
			<div className="row player-team-list">
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