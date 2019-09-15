import {Component, OnInit, ViewChild} from '@angular/core';
import {HttpService} from '../../services/http/http.service';
import {Hotkey, HotkeysService} from 'angular2-hotkeys';
import {Editor} from 'codemirror';

@Component({
  selector: 'app-core',
  templateUrl: './core.component.html',
  styleUrls: ['./core.component.css']
})
export class CoreComponent implements OnInit {
  @ViewChild('editor', {static: true}) editor: Editor;
  fileContent: string;
  currentLine: number;
  currentChar: number;
  tts = window.speechSynthesis;
  audioCtx = new window.AudioContext;
  editorConfigured = false;
  bpm = 120;
  introText = 'You are now in the editor. You can begin typing code now. Press control + enter when you are ready to run your program. To change your BPM, press control + shift';

  constructor(private httpService: HttpService, private hotkeyService: HotkeysService) {
    this.hotkeyService.add(new Hotkey('ctrl+enter', (): boolean => {
      this.submitCode();
      return false;
    }, ['INPUT', 'TEXTAREA']));
    this.hotkeyService.add(new Hotkey('ctrl+shift', (): boolean => {
      this.changeBpm();
      return false;
    }, ['INPUT', 'TEXTAREA']));
  }

  changeBpm() {
    const utter = new SpeechSynthesisUtterance();
    utter.text = 'Enter a new BPM value then press enter';
    utter.pitch = 0.5;
    utter.rate = 1;
    this.tts.speak(utter);
    this.bpm = +prompt('Enter a new BPM value');
  }

  ngOnInit() {
    console.log(this.tts.getVoices());
    const intro = new SpeechSynthesisUtterance();
    intro.text = this.introText;
    intro.pitch = 0.5;
    intro.rate = 1;
    if (this.tts.speaking) {
      this.tts.cancel();
    }
    this.tts.speak(intro);
    console.log(this.editor);
  }

  submitCode() {
    this.httpService.sendCode({
      code: this.fileContent,
      bpm: this.bpm
      }).subscribe((data: ArrayBuffer) => {
        const source = this.audioCtx.createBufferSource();
        this.audioCtx.decodeAudioData(data, (buffer)=> {
          source.buffer = buffer;
          source.connect(this.audioCtx.destination);
          source.start(0);
        });
      });
  }

  onCursorChange(editor: Editor) {
    if (!this.editorConfigured) {
      editor.setSize(null, '100vh');
      this.editorConfigured = true;
    }
    const newLine = editor.getDoc().getCursor().line;
    const newChar = editor.getDoc().getCursor().ch;
    let textToSpeak = '';
    let textSpeakRate = 1;
    if ((newLine > this.currentLine) || (newLine < this.currentLine)) {
      textToSpeak =  editor.getDoc().getLine(newLine);
      if (textToSpeak.includes('-')) {
        textToSpeak = textToSpeak.replace('-', 'Minus');
      }
      textSpeakRate = 1.5;
    } else if (newChar > this.currentChar) {
      textToSpeak = editor.getDoc().getRange({line: newLine, ch: newChar - 1}, {line: newLine, ch: newChar});
    } else if (newChar < this.currentChar) {
      textToSpeak = editor.getDoc().getRange({line: newLine, ch: newChar}, {line: newLine, ch: newChar + 1});
    }
    this.currentLine = newLine;
    this.currentChar = newChar;
    this.speakText(textToSpeak, textSpeakRate);
  }

  speakText(text: string, rate: number) {
    if ((text !== this.introText) && (text !== '')) {
      this.tts.cancel();
    }
    text = this.checkTextForSpecialChars(text);
    const utterance: SpeechSynthesisUtterance = new SpeechSynthesisUtterance();
    utterance.voice = this.tts.getVoices().find(voice => voice.name === 'en-US');
    utterance.text = text;
    // utterance.rate = 0.2;
    //utterance.pitch = 0.5;
    this.tts.speak(utterance);
    console.log(utterance.voice);

  }

  checkTextForSpecialChars(char: string): string {
    // God forgive me
    switch (char) {
      case '(':
        return 'LeftBracket';
      case ')':
        return 'RightBracket';
      case ' ':
        return 'Space';
      case '-':
        return 'Minus';
      default:
        return char;
    }
  }
}
