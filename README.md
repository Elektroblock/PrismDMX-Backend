# PrismDMX-Backend

## API Documentation:

- ### add newFixture:
```
    {"newFixture":{"name":"NAME","startChannel":"000","channels":[{"ChannelName":"NAME","ChannelType":"TYPE","dmxChannel":"CHANNEL"},{"ChannelName":"NAME","ChannelType":"TYPE","dmxChannel":"CHANNEL"}]}}
```

- ### editFixture
```
Coming Soon
```

- ### deleteFixture:
```
{"deleteFixture": "ID"}
```

- ### setProject:
```
{"setProject": "ID"}
```

- ### deleteProject:
```
{"deleteProject": "ID"}
```

- ### newProject:
```
{"newProject": "NAME"}
```

- ### newPage:
```
{"newPage": ""}
```

- ### deletePage:
```
{"deletePage": "ID"}
```

- ### editMixerFader
```
Coming Soon
```

- ### editMixerButton
```
Coming Soon
```

- ### setMixerColor:
```
{"setMixerColor": "#ffffff"}
```

- ### addFixtureToGroup:
```
{"addFixtureToGroup": {"groupID":"ID", "fixtureID":"ID"}}
```

- ### removeFixtureFromGroup:
```
{"removeFixtureFromGroup": {"groupID":"ID", "fixtureID":"ID"}}
```

- ### deleteGroup:
```
{"deleteGroup": "ID"}
```

- ### newGroup:
```
{"newGroup": "NAME"}
```

- ### selectFixture: WRONG DATA SRUCTURE
```
{"selectFixture": "ID"}
```

- ### deselectFixture: WRONG DATA SRUCTURE
```
{"deselectFixture": "ID"}
```

- ### selectFixtureGroup: WRONG DATA SRUCTURE
```
{"selectFixtureGroup": "ID"}
```

- ### deselectFixtureGroup: WRONG DATA SRUCTURE
```
{"deselectFixtureGroup": "ID"}
```