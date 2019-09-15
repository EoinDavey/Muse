import {Component, OnInit} from '@angular/core';
import {HttpService} from '../../services/http/http.service';
import {Hotkey, HotkeysService} from 'angular2-hotkeys';
import {Editor} from 'codemirror';

@Component({
  selector: 'app-core',
  templateUrl: './core.component.html',
  styleUrls: ['./core.component.css']
})
export class CoreComponent implements OnInit {
  fileContent: string;
  currentLine: number;
  currentChar: number;
  tts = window.speechSynthesis;
  editorConfigured = false;
  introText = 'You are now in the editor. You can begin typing code now. Press control + enter when you are ready to run your program.';

  constructor(private httpService: HttpService, private hotkeyService: HotkeysService) {
    this.hotkeyService.add(new Hotkey('ctrl+enter', (): boolean => {
      this.submitCode();
      return false; // Prevent bubbling
    }, ['INPUT', 'TEXTAREA']));
  }

  ngOnInit() {
    const intro = new SpeechSynthesisUtterance();
    intro.text = this.introText;
    intro.pitch = 0.5;
    intro.rate = 1;
    if (this.tts.speaking) {
      this.tts.cancel();
    }
    this.tts.speak(intro);
  }

  submitCode() {
    const utterance: SpeechSynthesisUtterance = new SpeechSynthesisUtterance();
    utterance.lang = 'en-US';
    utterance.voice = this.tts.getVoices().find(voice => voice.lang === 'en-US');
    utterance.text = this.fileContent;
    utterance.rate = 1.5;
    utterance.pitch = 0.5;
    this.tts.speak(utterance);
    this.httpService.sendCode({
      code: this.fileContent
    });
  }

  onCursorChange(editor: Editor) {
    if (!this.editorConfigured) {
      editor.setSize(null, '100vh');
      // editor.setOption('mode', 'calliope');
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
    utterance.voice = this.tts.getVoices().find(voice => voice.lang === 'en');
    utterance.text = text;
    utterance.rate = rate;
    utterance.pitch = 0.5;
    this.tts.speak(utterance);
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
