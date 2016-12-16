/*
*	Requires:
*		- JS-Cookie
*/
var PlayerForm = React.createClass({
	handleNameChange: function(event){
		this.setState({playerName: event.target.value});
	},
	handleSubmit: function(event){

		event.preventDefault();
		// Package Form Data
		var data = {
			username: this.state.playerName
		};

		// Extract CSRF and encode it in header
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
				}
			}
		});

		// Submit form via AJAX POST
		$.ajax({
			type: 'POST',
			url: this.props.endpoint,
			data: data,
			success: function(data) {
				window.location.href = this.props.successRedirect;
			}.bind(this),
			error: function(jqXhr) {
				console.log('failed to register');
			}.bind(this)
		});
	},
	render:function(){
		return(
			<div className="row team-form">
				<form onSubmit={this.handleSubmit}>
					<div className="small-0 medium-4 columns">
					</div>
					<div className="small-12 medium-4 columns">
						<input type="text" onChange={this.handleNameChange} placeholder="Enter User Name" maxLength={15} />
					</div>
					<div className="small-0 medium-4 columns">
					</div>
					<div className="row">
						<div className="small-0 medium-4 columns">
						</div>
						<div className="small-12 medium-4 columns">
							<button type="submit">Submit</button>
						</div>
						<div className="small-0 medium-4 columns">
						</div>
					</div>
				</form>
			</div>
		);
	}
});

var reactEntry = document.getElementById('react-player-form');
var userPK = reactEntry.getAttribute('data-userPK');
var endpoint= reactEntry.getAttribute('data-endpoint');
var successRedirect = reactEntry.getAttribute('data-successRedirect');

ReactDOM.render(
  <PlayerForm  endpoint={endpoint} successRedirect={successRedirect} />,
  document.getElementById('react-player-form')
);