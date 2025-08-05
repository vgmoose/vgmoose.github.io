---
layout: post
title: SwiftUI - Using callbacks to avoid delegates to update state from a UIViewControllerRepresentable or UIViewRepresentable (No Coordinators)
date: 2025-08-05 02:57:02
comments: true
categories: swift, coding, swiftui, callbacks
id: 4967421379
---

That is a mouthful of a post title!

There are some (really good!) articles on the Internet about how to communicate with a traditional UIView or UIViewController from a parent SwiftUI view. Like [this one](https://www.hackingwithswift.com/books/ios-swiftui/using-coordinators-to-manage-swiftui-view-controllers), or [this one](https://www.avanderlee.com/swiftui/integrating-swiftui-with-uikit/).

I have the impression though that they're coming at the problem from a UIKit perspective though, which makes sense given that a traditional UIView _is_ being used.

But if you find yourself unable to follow the way the Coordinator interacts with the delegate, and bridges the UIView <-> SwiftUI state variable (for example, the author of [this reddit post](https://www.reddit.com/r/SwiftUI/comments/i7paes/immense_confusion_and_despair_using_coordinators/)) try this!

```swift
// your parent SwiftUI view, and the state you want to update
struct ParentView: View {
    @State var myState = ""
    var body: some View {
        WrappedUIView(callback: { newValue in
            myState = newValue // this works!
        })
    }
    // ...rest of your view
}

// the wrapping view (aka the bridge) which hooks up the callback
// replace YourViewControllerClass with your target UIViewController
struct WrappedUIView: UIViewControllerRepresentable {
	typealias UIViewControllerType = YourViewControllerClass
	
	let callback: (String) -> Void // replace with your desired actual args/types
	
	func makeUIViewController(context: Context) -> YourViewControllerClass {
		let vc = YourViewControllerClass()
		vc.updateMyState = callback
		return vc
	}

	func updateUIViewController(_ uiViewController: YourViewControllerClass, context: Context) {
        // for moving in the other direction
	}
}

// then your UIViewController needs the callback defined as well
class YourViewControllerClass: UIViewController {
    // ...
    var updateMyState: (String) -> Void = { _ in } // replace with desired args/type
    // ...
}
```

I found doing it this way to be a lot easier to follow. You can then call it like a normal method, from YourViewControllerClass:

```swift
self.updateMyState("hello")
```

Will properly update the `myState` variable. So it both behaves how you _want_ it to behave, and properly interacts with the SwiftUI lifecycle.

The process is similar and also works for `UIViewRepresentable`, if you replace all occurrences of `UIViewControllerRepresentable` with it, and then use a `UIView` instead of a `UIViewController`. SwiftUI provides both.

Upon closer inspection, the Coordinator / delegate system _does_ make sense, but hopefully this code helps the process click for someone else. It's not as special as it seems! Callbacks work the way that you'd expect them.

And by initializing `YourViewControllerClass`'s `updateMyState` to `{ _ in }` you can avoid an optional as well. Be warned though, you might want to put a print there to ensure it's actually getting properly overriden.

The type `(String) -> Void`  can be changed to whatever you want (or `() -> Void` for no arguments).