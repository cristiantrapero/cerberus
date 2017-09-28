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

(load "../src/knowledge/scone-knowledge.d/load")


(define-test is-execute_authorised_command-an-event?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (is-x-a-y? {execute_authorised_command} {event}) :YES))

(define-test is-execute_authorised_command-an-action?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (is-x-a-y? {execute_authorised_command} {action}) :YES))

(define-test is-the-agent-of-execute_authorised_command-a-person?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (is-x-a-y? (the-x-role-of-y {action agent} {execute_authorised_command}) {person}) :YES))

(define-test is-the-object-of-execute_authorised_command-a-command?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (is-x-a-y? (the-x-role-of-y {action object} {execute_authorised_command}) {command}) :YES))

(define-test in-before-context-of-execute_authorised_command-a-command-is-recognized
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (car (cddadr (list-context-contents {execute_authorised_command BC})))
		(lookup-element {person is recognized in the scene})))
  
(define-test in-before-context-of-execute_authorised_command-a-person-is-recognized
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (caddar (list-context-contents {execute_authorised_command BC}))
		(lookup-element {command is recognized in the scene})))

(define-test in-after-context-of-execute_authorised_command-a-person-and-command-are-recognized
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (caddar (list-context-contents {execute_authorised_command AC}))
		(lookup-element {command executed by authorised person})))

(define-test is-the-Authenticator-service-instance-an-AuthenticatedCommandService?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (is-x-a-y? {Authenticator-service-instance} {AuthenticatedCommandService}) :YES))

(define-test is-setObserver-a-method-of-AuthenticatedCommandService?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (is-x-a-y-of-z? {Authenticator.setObserver} {implemented-method} {AuthenticatedCommandService})
		:YES))

(define-test is-notifyPerson-a-method-of-AuthenticatedCommandService?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (is-x-a-y-of-z? {Authenticator.notifyPerson} {implemented-method} {AuthenticatedCommandService})
		:YES))

(define-test is-notifyCommand-a-method-of-AuthenticatedCommandService?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (is-x-a-y-of-z? {Authenticator.notifyCommand} {implemented-method} {AuthenticatedCommandService})
		:YES))

;; (define-test is-identity-a-required-argument-of-notifyPerson?
;;     (in-context {dharma})
;;   (assert-equal *context* (lookup-element {dharma}))
;;   (assert-equal (is-x-a-y-of-z? {identity} {required-argument} {Authenticator.notifyPerson})
;; 		:YES))

;; (define-test is-command-a-required-argument-of-notifyCommand?
;;     (in-context {dharma})
;;   (assert-equal *context* (lookup-element {dharma}))
;;   (assert-equal (is-x-a-y-of-z? {command} {required-argument} {Authenticator.notifyCommand})
;; 		:YES))

(define-test what-event-causes-execute_authorised_command-action?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (list-causes {command execution by authorised person})
		(lookup-element {execute_authorised_command})))

(define-test what-method-causes-the-command_execution_by_authorised_person-event?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (get-the-method-that-causes-event {command execution by authorised person})
		(lookup-element {DigitalSink.notify})))

(define-test what-method-performs-execute_authorised_command-action?
    (in-context {dharma})
  (assert-equal *context* (lookup-element {dharma}))
  (assert-equal (get-the-method-that-performs-action {execute_authorised_command})
		(lookup-element {Authenticator.notifyCommand})))
