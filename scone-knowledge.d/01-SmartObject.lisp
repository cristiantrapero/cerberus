(new-type {metadata} {information object})
(new-type {byteseq} {information object})
(new-is-a {image format} {information object})
(new-type {boolean} {information object})


;; Observable
(new-type {Observable} {dharma-interface})
(new-type {Observable.setObserver} {dharma-method})
(x-is-a-y-of-z {Observable.setObserver} {implemented-method} {Observable})

;; DigitalSink
(new-type {DigitalSink} {dharma-interface})
(new-type {DigitalSink.notify} {dharma-method})
(x-is-a-y-of-z {DigitalSink.notify} {implemented-method} {DigitalSink})

;; EventSink
(new-type {EventSink} {dharma-interface})
(new-type {EventSink.notify} {dharma-method})
(x-is-a-y-of-z {EventSink.notify} {implemented-method} {EventSink})

;; SnapshotService
(new-type {SnapshotService} {dharma-service})
(new-is-a {SnapshotService} {Observable})
(new-is-a {SnapshotService} {EventSink})

;; ClipService
(new-type {ClipService} {dharma-service})
(new-is-a {ClipService} {Observable})
(new-is-a {ClipService} {EventSink})

;; DataSink
(new-type {DataSink} {dharma-service})
(new-type {DataSink.trigger} {dharma-method})

;; FaceDetector
(new-type {FaceDetector} {dharma-service})
(new-is-a {FaceDetector} {DataSink})
(new-is-a {FaceDetector} {Observable})

;; PersonRecognizer
(new-type {PersonRecognizer} {dharma-service})
(new-is-a {PersonRecognizer} {DataSink})
(new-is-a {PersonRecognizer} {Observable})

;; SpeechToText
(new-type {SpeechToText} {dharma-service})
(new-is-a {SpeechToText} {DataSink})
(new-is-a {SpeechToText} {Observable})
(new-type {SpeechToText.trigger} {dharma-method})
(x-is-a-y-of-z {SpeechToText.trigger} {implemented-method} {SpeechToText})

;; AuthenticatedCommandService
(new-type {AuthenticatedCommandService} {dharma-service})
(new-is-a {AuthenticatedCommandService} {Observable})
(new-type {AuthenticatedCommandService.notifyPerson} {dharma-method})
(new-type {AuthenticatedCommandService.notifyCommand} {dharma-method})
(x-is-a-y-of-z {AuthenticatedCommandService.notifyPerson} {implemented-method} {AuthenticatedCommandService})
(x-is-a-y-of-z {AuthenticatedCommandService.notifyCommand} {implemented-method} {AuthenticatedCommandService})
