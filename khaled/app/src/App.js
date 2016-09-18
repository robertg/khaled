import React, { Component } from 'react';
import AudioRecorder from 'react-audio-recorder';
import Webcam from 'react-webcam';

import noise from './noise.png';
import './App.css';

class App extends Component {
  state = {
    done: false,
  };

  handleChangeAudio = (duration, data) => {
    this.setState({done: !this.state.done});
    console.log('yo', duration, data);
  };

  renderFilters() {
    if (!this.state.done) {
      return null;
    }

    return (
      <div className="filters">
        <button className="filter harambe" />
        <button className="filter khaled" />
        <button className="filter trump" />
        <button className="filter bean" />
        <button className="filter yang" />
      </div>
    );
  }

  render() {
    return (
      <div className="App">
        <div className="blur">
          <Webcam className="webcam" audio={false} />
        </div>
        <img className="noise" src={noise} />
        <div className="darkLayer" />
        <div className="title">SOUNDCHAT</div>
        <div className="main">
          <div className="wrapper">
            <Webcam className="video" audio={false} height={null} width={null} />
          </div>
        </div>
        <div className="controls">
          {this.renderFilters()}
          <AudioRecorder
            onChange={this.handleChangeAudio}
            strings={{remove: '❌', download: '💾'}}
          />
        </div>
      </div>
    );
  }
}

export default App;
