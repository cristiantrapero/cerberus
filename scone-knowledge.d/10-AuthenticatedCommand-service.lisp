(in-context {dharma})

(new-action-type {execute_authorised_command}
		 :agent-type {person}
		 :object-type {command})

(new-context {execute_authorised_command bc} {dharma})
(new-is-a {execute_authorised_command bc} {before context})
(x-is-the-y-of-z {execute_authorised_command BC} {before context} {execute_authorised_command})

(new-context {execute_authorised_command ac} {execute_authorised_command bc})
(new-is-a {execute_authorised_command ac} {after context})
(x-is-the-y-of-z {execute_authorised_command ac} {after context} {execute_authorised_command})

(in-context {execute_authorised_command BC})
(new-indv {command is recognized in the scene} {command recognition})
(new-indv {person is recognized in the scene} {person recognition})

(in-context {execute_authorised_command AC})
(new-indv {command executed by authorised person} {command execution by authorised person})


(in-context {dharma})
(new-indv {Authenticator-service-instance} {AuthenticatedCommandService})
(new-indv {Authenticator.setObserver} {dharma-method})
(new-is-a {Authenticator.setObserver} {Observable.setObserver})
(new-indv {Authenticator.notifyPerson} {dharma-method})
(new-is-a {Authenticator.notifyPerson}  {AuthenticatedCommandService.notifyPerson})
(new-indv {Authenticator.notifyCommand} {dharma-method})
(new-is-a {Authenticator.notifyCommand}  {AuthenticatedCommandService.notifyCommand})
(x-is-a-y-of-z {Authenticator.setObserver} {implemented-method} {Authenticator-service-instance})
(x-is-a-y-of-z {Authenticator.notifyPerson} {implemented-method} {Authenticator-service-instance})
(x-is-a-y-of-z {Authenticator.notifyCommand} {implemented-method} {Authenticator-service-instance})

;; (x-is-a-y-of-z {identity} {required-argument} {Authenticator.notifyPerson})
;; (x-is-a-y-of-z {command} {required-argument} {Authenticator.notifyCommand})

;;(new-statement {person recognition} {happens before} {command recognition})
;; (x-is-a-y-of-z {person recognition} {subevent} {command execution by authorised person})
;; (x-is-a-y-of-z {command recognition} {subevent} {command execution by authorised person})

(new-statement {Authenticator-service-instance}  {performs action through} {execute_authorised_command} :c {Authenticator.notifyCommand})
(new-statement {execute_authorised_command} {causes} {command execution by authorised person})

(new-statement {Authenticator-service-instance} {causes event through} {command execution by authorised person} :c {DigitalSink.notify})


(new-indv {authenticator} {proxy})
(x-is-the-y-of-z {authenticator} {service-proxy} {Authenticator-service-instance})
