/* Online Offline Orb */
var TeammateStatus = React.createClass({
	render: function(){
		// Player's status (props.data) online? T/F
		if(this.props.data == false){
			return (<p className="teammate-status-offline">x</p>);
		}

		return (<p className="teammate-status-online">o</p>);
	}
});

/* Teammate P-Tag w/ Color based on Online state */
var TeammateName = React.createClass({
	getInitialState: function(){
  	return {
    	classNm:""
    };
  },
	render: function(){
		// Check teammate status
		if(this.props.data['status'] == false){
			// User is offline
			this.state.classNm = "teammate-name teammate-name-offline";
		} else {
			// User is online
			this.state.classNm = "teammate-name teammate-name-online";
		}

		return (<p className={this.state.classNm}>{this.props.data['name']}</p>);
	}
});

/* Panel that lists teammates and their online status */
var TeammateList = React.createClass({
	getInitialState: function(){
		return {data:[{name:'Austin', status:true}, {name:'Jon', status:false}, {name:'Keeson', status:true}, {name:'Dusty', status:false}, {name:'Cory', status:true}]};
	},
	render: function(){
		// Returns name & status panel for each teammate string passed in
		var teammate_panels = this.state.data.map(function(teammate){
			return (
				<div className="row teammate-row">
					<div className="small-10 columns teammate-name-panel">
						<TeammateName className="teammate-name" data={teammate} />
					</div>
					<div className="small-2 columns teammate-status-panel">
						<TeammateStatus className="teammate-status" data={teammate['status']} />
					</div>
				</div>
			);
		});

		return(
			<div className="teammate">
				{teammate_panels}
			</div>
		);
	}
});


/* Panel for listing a singular team */
var TeamPanel = React.createClass({
  	getInitialState: function(){
    	return {isOnline: true};
    },
    render: function(){
      // data{ 'teammates':{...teammates...}, 'teamname':'name'}
      var teammates = this.props.data['teammates'];

    	for(var i = 0; i < teammates.length; i++){
      		if(teammates[i]['status'] == false){
      			this.state.isOnline = false;
      			break;
      		}
      		this.state.isOnline = true;
    	}

    	if(this.state.isOnline){
			return (<p className="team-name team-online">{this.props.data['teamname']}</p>);
		} else {
    		return (<p className="team-name team-offline">{this.props.data['teamname']}</p>);
   		}
	}
});

var TeamEntryButton = React.createClass({
	render: function(){
		return(
			<button className="team-list-btn">{this.props.teamName}</button>
		);
	}
});

var TeamList = React.createClass({
	getInitialState: function(){
		return{data:[ {team:'Monochrome', players:[{name:'Jon', status:true}, {name:'Austin', status:false}]},
					  {team:'Fnatic', players:[{name:'CoolMatt69', status:true}, {name:'Austin', status:false}]} ]};
	},
	render: function(){
		var teamList = this.state.data.map(function(teamNode){
	    	return(
				<div className="row">
					<div className="small-12 columns">
						<TeamEntryButton teamName={teamNode['team']} />
					</div>
				</div>
	       	);
		});
		return (teamList);
	}
});

// Server Info ---> TeamWidget --> TeamList --> Team --> TeammateList / Status



