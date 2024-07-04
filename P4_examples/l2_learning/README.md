# L2 Learning

```
+--+      +--+     ++-+
|h1+------+  +-----+h2+
+--+      +  +     +--+
          +s1+
+--+      +  +     ++-+
|h3+------+  +-----+h4+
+--+      +-++     +--+

```

## Introduction

In this example you can see how to use copy to cpu or digests to implement
a l2 learning P4 application and controller. You can find a better explained version
of this example in the [exercises](../../exercises/04-L2_Learning) section.

## TODO
1. change the `l2_learning_controller.py` to the `FOP4` version.
2. 


## How to run

### Digest-based L2 Learning

1. Start the topology (this will also compile and load the program).

   ```bash
   sudo python3 network.py
   ```

2. Start the controller in another terminal window:

   ```bash
   sudo python3 l2_learning_controller.py s1
   ```

   We tell the controller from which switch listen from. The `digest` parameter tells the controller which technique it should
   use to receive packets. In this case it will use the `nanomsg` socket to receive digests.