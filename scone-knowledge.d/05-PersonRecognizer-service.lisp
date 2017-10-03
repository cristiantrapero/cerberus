(in-context {dharma})

(new-action-type {recognize_person}
		 :agent-type {recognizer}
		 :object-type {person})

(new-context {recognize_person bc} {dharma})
(new-is-a {recognize_person bc} {before context})
(x-is-the-y-of-z {recognize_person BC} {before context} {recognize_person})
(new-context {recognize_person ac} {recognize_person bc})
(new-is-a {recognize_person ac} {after context})
(x-is-the-y-of-z {recognize_person ac} {after context} {recognize_person})

(in-context {recognize_person BC})
(new-indv {person appears in the scene} {motion detected})
(in-context {recognize_person AC})
(new-indv {assigned ID} {thing})
(x-is-the-y-of-z  {assigned ID} {identity} (the-x-role-of-y {action object} {recognize_person}))


(in-context {dharma})
(new-indv {PersonRecognizer-service-instance} {PersonRecognizer})
(new-indv {PersonRecognizer.setObserver} {dharma-method})
(new-is-a {PersonRecognizer.setObserver} {Observable.setObserver})
(new-indv {PersonRecognizer.trigger} {dharma-method})
(new-is-a {PersonRecognizer.trigger}  {DataSink.trigger})
(x-is-a-y-of-z {PersonRecognizer.setObserver} {implemented-method} {PersonRecognizer-service-instance})
(x-is-a-y-of-z {PersonRecognizer.trigger} {implemented-method} {PersonRecognizer-service-instance})
(x-is-a-y-of-z {jpg} {required-argument} {PersonRecognizer.trigger})

(new-type {person recognition when person detected} {sequential event})
;(new-statement {motion detected} {happens before} {person recognition})
(x-is-a-y-of-z {motion detected} {subevent} {person recognition when person detected})
(x-is-a-y-of-z {person recognition} {subevent} {person recognition when person detected})


(new-statement {PersonRecognizer-service-instance}  {performs action through} {recognize_person}
	       :c {PersonRecognizer.trigger})

(new-statement {recognize_person} {causes} {person recognition})
(new-statement {PersonRecognizer-service-instance} {causes event through} {person recognition}
	       :c {AuthenticatedCommandService.notifyPerson})

;; Esto es temporal para testear el cliente
(new-indv {person-recognizer} {proxy})
(x-is-the-y-of-z {person-recognizer} {service-proxy} {PersonRecognizer-service-instance})


;; CL-USER> (list-causes {person recognition})
;; {recognize_person}
;; CL-USER> (list-rel-inverse {performs action through} {recognize_person})
;; ({PersonRecognizer-service-instance})
;; CL-USER> (c-element  {performs action through})
;; {C-role of performs action through 0-2621}
;; CL-USER> (list-children  {C-role of performs action through 0-2621})
;; ({PersonRecognizer.trigger})
