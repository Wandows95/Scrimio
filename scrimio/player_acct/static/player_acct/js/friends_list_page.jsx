/*
*	Requires:
*		- JS-Cookie
*/

var FriendEntry = React.createClass({
	render:function(){
		return(
		<div className="row data-friend-row">
			<div className="columns small-10">
				<p>{this.props.username}</p>
			</div>
			<div className="columns small-2">
				<p>{this.props.isOnline}</p>
			</div>
		</div>
		);
	}
});


var FriendsList = React.createClass({
	getInitialState:function() {
		return({friends:[]})	
	},
	componentDidMount: function(){
		// Submit form via AJAX POST
		$.ajax({
			type: 'GET',
			url: this.props.endpoint,
			success: function(data) {
				this.setState({friends: data.friends})
				console.log(this.state.friends)
			}.bind(this)
		});
	},
	render:function(){
		var friendsList = this.state.friends.map(function(friend){
			console.log("Online " + friend.is_online);
			return <FriendEntry username={friend.username} isOnline={friend.is_online.toString()} />
		});

		return(<div>{friendsList}</div>);
	}
});

var reactEntry = document.getElementById('react-friends-list');
var endpoint= reactEntry.getAttribute('data-endpoint');

ReactDOM.render(
  <FriendsList  endpoint={endpoint} />,
  reactEntry
);