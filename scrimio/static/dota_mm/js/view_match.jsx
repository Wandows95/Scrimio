var TeammateEntry = React.createClass({
	render:function(){
		return (
			<div is class="row team-entry-row">
				<div is class="small-6 columns callout panel">
					<h3>{this.props.playerName}</h3>
				</div>
			</div>
		);
	}
});

var TeamPlayerList = React.createClass({
	getInitialState: function(){
		return({teams:[{"captain":{"username":"test"}}]});
	},
	componentDidMount:function(){
		$.ajax({
			dataType:"JSON",
			url: this.props.endpoint,
			success:function(data){
				this.setState({teams: data.teams});
			}.bind(this)
		});
	},
	render: function(){
		/*var playerList = this.state.teams[0]["captain"].map(function(player){
			return <TeamEntry playerName={player.username} />
		});*/
		//var playerList = <TeammateEntry playerName={this.state.teams[0]['captain']['username']} />

		return(
			<div className="row player-team-list">
				<div className="row player-team-list-header">
					<div className="small-6 columns team-entry-header-name">
						<h2>Team 1</h2>
					</div>
				</div>
				<TeammateEntry playerName={this.state.teams[0].captain.username} />
				<TeammateEntry playerName={""} />
				<TeammateEntry playerName={""} />
				<TeammateEntry playerName={""} />
				<TeammateEntry playerName={""} />
			</div>
			
		);
	}
});

var reactEntry = document.getElementById('react-match-view');

ReactDOM.render(
  <TeamPlayerList endpoint={reactEntry.getAttribute('data-endpoint')} />,
  document.getElementById('react-match-view')
);