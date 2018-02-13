;;   Copyright 2013 Google Inc.
;;
;;   Licensed under the Apache License, Version 2.0 (the "License");
;;   you may not use this file except in compliance with the License.
;;   You may obtain a copy of the License at
;;
;;       http://www.apache.org/licenses/LICENSE-2.0
;;
;;   Unless required by applicable law or agreed to in writing, software
;;   distributed under the License is distributed on an "AS IS" BASIS,
;;   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
;;   See the License for the specific language governing permissions and
;;   limitations under the License.


; Concept: What do you do to go through the lisp koans?  You fill in
; the blanks, or otherwise fix the lisp code so that the
; code within the 'define-test' blocks passes.


; In common lisp, "True" and "False" are represented by "t" and "nil".
; More in a future lesson, but for now, consider t to be true,
; and nil to be false.

(load "../src/scone-knowledge.d/load")

(define-test is-capture_audio-an-event?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (is-x-a-y? {capture_audio} {event}) :YES))

(define-test is-capture_audio-an-action?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (is-x-a-y? {capture_audio} {action}) :YES))

(define-test is-the-agent-of-capture_audio-a-microphone?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (is-x-a-y? (the-x-role-of-y {action agent} {capture_audio}) {microphone}) :YES))

(define-test is-the-object-of-capture_audio-the-sound?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (is-x-a-y? (the-x-role-of-y {action object} {capture_audio}) {sound}) :YES))

(define-test in-before-context-of-capture_audio-a-motion-is-detected
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (car (cddar (list-context-contents {capture_audio BC})))
		(lookup-element {sound appears in the scene})))

(define-test in-after-context-of-capture_audio-an-audio-file-is-recorded
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (caddar (list-context-contents {capture_audio AC}))
		(lookup-element {recorded audio})))
