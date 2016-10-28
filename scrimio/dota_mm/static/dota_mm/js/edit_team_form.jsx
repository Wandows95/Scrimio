/*
*	Requires:
*		- JS-Cookie
*/
var TeamForm = React.createClass({
	getInitialState: function(){
		return ({})
	},
	componentDidMount: function(){
		//console.log("Component Mounted");
		var data = [];

		$.ajax({
			type: 'GET',
			url: this.props.getEndpoint,	// API Endpoint
			data: data,
			success: function(data) {	// Fill state data on component
				this.setState({teamName: data["name"]});
				this.setState({teamDescription: data["description"]});
			}.bind(this),
			error: function(jqXhr) {
				console.log('failed to register');
			}.bind(this)
		});
	},
	handleDescriptionChange: function(event){
		this.setState({teamDescription: event.target.value});
	},
	handleDelete: function(event){
		event.preventDefault();

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
			type: 'DELETE',
			url: this.props.deleteEndpoint,
			success: function(data) {
				window.location.href = this.props.deleteRedirect;
			}.bind(this),
			error: function(jqXhr) {
				console.log('failed to register');
			}.bind(this)
		});
	},
	handleSubmit: function(event){

		event.preventDefault();
		// Package Form Data
		var data = {
			description: this.state.teamDescription
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
			type: 'PATCH',
			url: this.props.postEndpoint,
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
					<div className="small-12 medium-6 columns">
						<input type="text" value={this.state.teamName}  maxLength={20} />
					</div>
					<div className="row">
						<div className="small-12 medium-6 columns">
							<textarea name="team-description" placeholder="Team Description" value={this.state.teamDescription} onChange={this.handleDescriptionChange} className="team-description-text" />
						</div>
					</div>
					<div className="row">
						<div className="small-6 columns">
							<button type="submit">Submit</button>
						</div>
						<div className="small-6 columns" >
							<button onClick={this.handleDelete}>DELETE</button>
						</div>
					</div>
				</form>
			</div>
		);
	}
});

var reactEntry = document.getElementById('react-team-form');

ReactDOM.render(
  <TeamForm postEndpoint={reactEntry.getAttribute('data-post-endpoint')} getEndpoint={reactEntry.getAttribute('data-get-endpoint')} 
  successRedirect={reactEntry.getAttribute('data-successRedirect')} deleteEndpoint={reactEntry.getAttribute('data-delete-endpoint')} userPK={reactEntry.getAttribute('data-userPK')} />,
  document.getElementById('react-team-form')
);