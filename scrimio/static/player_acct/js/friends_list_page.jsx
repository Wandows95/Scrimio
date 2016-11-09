/*
*	Requires:
*		- JS-Cookie
*/

var FriendEntry = React.createClass({
	render:function(){
		return(
		<div class="row data-friend-row">
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
	componentDidMount: function(){
		// Submit form via AJAX POST
		$.ajax({
			type: 'GET',
			url: this.props.endpoint,
			success: function(data) {
				this.setState({friends: data.friends})
			}.bind(this)
			error: function(jqXhr) {
				console.log('failed to register');
			}.bind(this)
		});
	},
	render:function(){
		var friendsList = state.friends.map(function(friend){
			return <FriendEntry username={friend.username} isOnline={friend.is_online} />
		});

		return({friendsList});
	}
});

var reactEntry = document.getElementById('react-friends-list');
var endpoint= reactEntry.getAttribute('data-endpoint');

ReactDOM.render(
  <FriendsList  endpoint={endpoint} />,
  reactEntry
);