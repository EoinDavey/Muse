import { Component, OnInit } from '@angular/core';
import {Hotkey, HotkeysService} from 'angular2-hotkeys';
import {Router} from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  tts = window.speechSynthesis;

  constructor(private hotkeyService: HotkeysService, private  router: Router) {
    this.hotkeyService.add(new Hotkey('ctrl+enter', (): boolean => {
      this.router.navigate(['/editor']).then();
      return false;
    }, ['INPUT', 'TEXTAREA']));
  }

  ngOnInit() {
    const intro = new SpeechSynthesisUtterance();
    intro.text = 'Welcome to Muse. You can press control + enter to go straight to the editor!';
    intro.pitch = 0.5;
    intro.rate = 1;
    if (this.tts.speaking) {
      this.tts.cancel();
    }
    this.tts.speak(intro);
  }

}
