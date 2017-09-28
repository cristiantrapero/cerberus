(in-context {dharma})

(new-action-type {recognize_command}
		 :agent-type {recognizer}
		 :object-type {audio file}
		 :recipient-type {person})

(new-context {recognize_command bc} {dharma})
(new-is-a {recognize_command bc} {before context})
(x-is-the-y-of-z {recognize_command BC} {before context} {recognize_command})
(new-context {recognize_command ac} {recognize_command bc})
(new-is-a {recognize_command ac} {after context})
(x-is-the-y-of-z {recognize_command ac} {after context} {recognize_command})

(in-context {recognize_command BC})
(new-indv {person talking the scene} {motion detected})
(in-context {recognize_command AC})


(in-context {dharma})
(new-indv {SpeechToText-service-instance} {SpeechToText})
(new-indv {SpeechToText.setObserver} {dharma-method})
(new-is-a {SpeechToText.setObserver} {Observable.setObserver})
(new-is-a {SpeechToText.trigger}  {DataSink.trigger})
(x-is-a-y-of-z {SpeechToText.setObserver} {implemented-method} {SpeechToText-service-instance})
(x-is-a-y-of-z {SpeechToText.trigger} {implemented-method} {SpeechToText-service-instance})
(x-is-a-y-of-z {wav} {required-argument} {SpeechToText.trigger})
(x-is-a-y-of-z {command} {returned-value} {SpeechToText.trigger})



(new-statement {SpeechToText-service-instance}  {performs action through} {recognize_command}
	       :c {SpeechToText.trigger})

(new-statement {recognize_command} {causes} {command recognition})
(new-statement {SpeechToText-service-instance} {causes event through} {command recognition}
	       :c {AuthenticatedCommandService.notifyCommand})

;; Esto es temporal para testear el cliente
(new-indv {speech_to_text -t -e 1.1:tcp -h localhost -p 9004 -t 60000} {proxy})
(x-is-the-y-of-z {speech_to_text -t -e 1.1:tcp -h localhost -p 9004 -t 60000} {service-proxy} {SpeechToText-service-instance})


;; CL-USER> (list-causes {person recognition})
;; {recognize_command}
;; CL-USER> (list-rel-inverse {performs action through} {recognize_command})
;; ({SpeechToText-service-instance})
;; CL-USER> (c-element  {performs action through})
;; {C-role of performs action through 0-2621}
;; CL-USER> (list-children  {C-role of performs action through 0-2621})
;; ({SpeechToText.trigger})
