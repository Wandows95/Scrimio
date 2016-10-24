var TeamView = React.createClass({
	getInitialState: function(){
		return({teamName: "", teamDescription: "", teamElo:""})
	},
	componentDidMount: function(){
		console.log(this.props.endpoint);
		$.ajax({
			dataType:"JSON",
			url: this.props.endpoint,
			success: function(data){
				this.setState({teamName: data.name});
				this.setState({teamDescription: data.description});
				this.setState({teamElo: data.elo});
			}.bind(this)
		});
	},
	render: function(){
		return(
			<div className="row team-view">
				<div className="small-12 columns no-padding">
					<h1>{this.state.teamName}</h1>
				</div>
				<div className="row">
					<div className="small-12 medium-8 columns">
						<p>{this.state.teamDescription}</p>
					</div>
					<div className="small-12 medium-4 columns">
						<p>Team Elo: {this.state.teamElo}</p>
					</div>
				</div>
			</div>
		);
	}
});

var reactEntry = document.getElementById('react-team-view');

ReactDOM.render(
  <TeamView endpoint={reactEntry.getAttribute('data-endpoint')} />,
  document.getElementById('react-team-view')
);