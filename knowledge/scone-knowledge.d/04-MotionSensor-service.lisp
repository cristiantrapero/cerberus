(in-context {dharma})

(new-action-type {detect_motion}
		 :agent-type {sensor}
		 :object-type {motion}
		 :recipient-type {animate})
(new-context {detect_motion bc} {dharma})
(new-is-a {detect_motion bc} {before context})
(x-is-the-y-of-z {detect_motion BC} {before context} {detect_motion})
(new-context {detect_motion ac} {detect_motion bc})
(new-is-a {detect_motion ac} {after context})
(x-is-the-y-of-z {detect_motion ac} {after context} {detect_motion})

(in-context {detect_motion BC})
(new-not-statement (the-x-role-of-y {action object} {detect_motion}) {is detected in}  (the-x-role-of-y {action recipient} {detect_motion}))
(in-context {detect_motion AC})
(new-statement (the-x-role-of-y {action object} {detect_motion}) {is detected in}  (the-x-role-of-y {action recipient} {detect_motion}))

(in-context {dharma})
(new-indv {MotionSensor-service-instance} {Observable})
(new-indv {MotionSensor.setObserver} {dharma-method})
(new-is-a {MotionSensor.setObserver} {Observable.setObserver})
(x-is-a-y-of-z {MotionSensor.setObserver} {implemented-method} {MotionSensor-service-instance})

(new-statement {detect_motion} {causes} {motion detected})
(new-statement {MotionSensor-service-instance} {causes event through} {motion detected}
	       :c {EventSink.notify})

;; Esto es temporal para testear el cliente
(new-indv {motion_sensor -t -e 1.1:tcp -h localhost -p 9000 -t 60000} {proxy})
(x-is-the-y-of-z {motion_sensor -t -e 1.1:tcp -h localhost -p 9000 -t 60000} {service-proxy} {MotionSensor-service-instance})
