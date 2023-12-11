# Changelog


## [8.1.0](https://github.com/muhlba91/onyx-client/compare/v8.0.2...v8.1.0) (2023-12-11)


### Features

* replace linters with ruff ([36bea9d](https://github.com/muhlba91/onyx-client/commit/36bea9d83020c63af1c6713984c13430b6406da8))


### Bug Fixes

* add dimmable light mapping ([bd85d11](https://github.com/muhlba91/onyx-client/commit/bd85d11091049d5a1dbf1c2d180a329fe1dd5e1e))
* add tests for pergola and awning ([d9fb32c](https://github.com/muhlba91/onyx-client/commit/d9fb32cf6c9f65f57a4028375559d90933b45331))


### Miscellaneous Chores

* **ci:** adopt release please for v4 ([d14c22e](https://github.com/muhlba91/onyx-client/commit/d14c22e39ba3156db7d29b6432689b6c86c9c557))
* **ci:** update poetry version ([271c1da](https://github.com/muhlba91/onyx-client/commit/271c1daf8e37fe707f87c03fce54a78b20556c99))
* **deps:** update actions/setup-python action to v5 ([3b4d1ba](https://github.com/muhlba91/onyx-client/commit/3b4d1bab5d206aeafe1a8b85dbf8cefc994b508f))
* **deps:** update dependency aiohttp to v3.9.0 ([c3967c2](https://github.com/muhlba91/onyx-client/commit/c3967c280088e9508584dd3d12526a31bfb3d053))
* **deps:** update dependency aiohttp to v3.9.1 ([84fa5c9](https://github.com/muhlba91/onyx-client/commit/84fa5c9d27c24bed7dab37355047f89be5103085))
* **deps:** update dependency aioresponses to v0.7.6 ([ed3a04d](https://github.com/muhlba91/onyx-client/commit/ed3a04d3d76467faf2efd086d771d6f67fe402a3))
* **deps:** update dependency pre-commit to v3.6.0 ([bc65cf2](https://github.com/muhlba91/onyx-client/commit/bc65cf2db9e2f5374de29d3958e5c928bda37125))
* **deps:** update dependency pytest-asyncio to ^0.23.0 ([d92aa9b](https://github.com/muhlba91/onyx-client/commit/d92aa9b1844b7d44dada09da47b67744d5881168))
* **deps:** update dependency pytest-asyncio to v0.23.1 ([63ae0af](https://github.com/muhlba91/onyx-client/commit/63ae0afe77f91c64cddc44108533f08d4dc9745d))
* **deps:** update dependency pytest-asyncio to v0.23.2 ([8cb25b3](https://github.com/muhlba91/onyx-client/commit/8cb25b3436a34483322216bd1f8ca5749fbc123b))
* **deps:** update dependency ruff to v0.1.7 ([e87dc27](https://github.com/muhlba91/onyx-client/commit/e87dc27a38119249d0bf3ba893d39f6bae1103a5))
* **deps:** update google-github-actions/release-please-action action to v4 ([49badce](https://github.com/muhlba91/onyx-client/commit/49badcecf1862b4e9414a81e212e7f1f0b6d4cdf))

## [8.0.2](https://github.com/muhlba91/onyx-client/compare/v8.0.1...v8.0.2) (2023-11-17)


### Bug Fixes

* make log messages clearer for streaming ([a65d0d9](https://github.com/muhlba91/onyx-client/commit/a65d0d9f5d3c98d7f4aac9c4615536c848e2b626))

## [8.0.1](https://github.com/muhlba91/onyx-client/compare/v8.0.0...v8.0.1) (2023-11-17)


### Bug Fixes

* fix timeout and restart of read loop ([5e669bc](https://github.com/muhlba91/onyx-client/commit/5e669bc119935ca6264738891b2b90129f027739))

## [8.0.0](https://github.com/muhlba91/onyx-client/compare/v7.2.1...v8.0.0) (2023-11-17)


### ⚠ BREAKING CHANGES

* adds new method to listen for events in the background

### Features

* implement listening to events endpoint using callbacks ([330dd41](https://github.com/muhlba91/onyx-client/commit/330dd41964175ebb98a6f995e83c431805abde6d))


### Miscellaneous Chores

* **deps:** update pre-commit ([3a52c1e](https://github.com/muhlba91/onyx-client/commit/3a52c1e83492a70334b2e486509a075747e029b8))

## [7.2.1](https://github.com/muhlba91/onyx-client/compare/v7.2.0...v7.2.1) (2023-11-15)


### Bug Fixes

* fix aiohttp version to align with homeassistant ([d5c7634](https://github.com/muhlba91/onyx-client/commit/d5c763479dc01a91dd4596f4f022de1644350cd1))

## [7.2.0](https://github.com/muhlba91/onyx-client/compare/v7.1.1...v7.2.0) (2023-11-15)


### Features

* use real values for weather device tests ([d9a4e5e](https://github.com/muhlba91/onyx-client/commit/d9a4e5e48ff7c832e211f731f32742fd0a90f55e))


### Miscellaneous Chores

* **deps:** update actions/checkout action to v4 ([5beccd3](https://github.com/muhlba91/onyx-client/commit/5beccd32c11f58edc1a87a5c15cebed60611d612))
* **deps:** update dependency aiohttp to v3.8.6 ([633284e](https://github.com/muhlba91/onyx-client/commit/633284e8de57a463c1d18f79d06d2e2b0f69e8e1))
* **deps:** update dependency aioresponses to v0.7.5 ([a76bfc3](https://github.com/muhlba91/onyx-client/commit/a76bfc3a0fd13273eb5dc5f9001bdc4297525e4e))
* **deps:** update dependency black to v23.10.0 ([b21e719](https://github.com/muhlba91/onyx-client/commit/b21e7194d0c0ac245428953e5847cde6718af677))
* **deps:** update dependency black to v23.10.1 ([71b57b9](https://github.com/muhlba91/onyx-client/commit/71b57b947c2656c9367d0f58811ef44b3463b624))
* **deps:** update dependency black to v23.11.0 ([7134dc4](https://github.com/muhlba91/onyx-client/commit/7134dc403f639a50e87d3603bedcf5daba0086b7))
* **deps:** update dependency black to v23.9.0 ([7630c03](https://github.com/muhlba91/onyx-client/commit/7630c03fe3feae5a5b70b512ed28e7e7cac7911d))
* **deps:** update dependency black to v23.9.1 ([9beb2b0](https://github.com/muhlba91/onyx-client/commit/9beb2b033308868577a9e73fcdde22e1a5e9337a))
* **deps:** update dependency coverage to v7.3.1 ([1b90fcc](https://github.com/muhlba91/onyx-client/commit/1b90fcc2ef6d2b5f6bfadc9fdd8543cf995f532d))
* **deps:** update dependency coverage to v7.3.2 ([0d1b304](https://github.com/muhlba91/onyx-client/commit/0d1b304d6238bb427527d70a44fbe79142ddd625))
* **deps:** update dependency pre-commit to v3.4.0 ([6946b3c](https://github.com/muhlba91/onyx-client/commit/6946b3c31b3d906ec7708fab538e652391b1ae56))
* **deps:** update dependency pre-commit to v3.5.0 ([69ea510](https://github.com/muhlba91/onyx-client/commit/69ea510be6f861085d5098918a26969fddbcccf5))
* **deps:** update dependency pytest to v7.4.1 ([db60906](https://github.com/muhlba91/onyx-client/commit/db609065c2c011a1fc53ee5417c939a15864665c))
* **deps:** update dependency pytest to v7.4.2 ([a051c07](https://github.com/muhlba91/onyx-client/commit/a051c07dd6b93a5b2b56e5b795ab97cfa002997a))
* **deps:** update dependency pytest to v7.4.3 ([537384e](https://github.com/muhlba91/onyx-client/commit/537384e172c735ba4a29a04f2d968e57ff248ea1))
* **deps:** update dependency pytest-asyncio to ^0.22.0 ([789c7ce](https://github.com/muhlba91/onyx-client/commit/789c7ceec140883d85478f1a77a21915fbd57881))

## [7.1.1](https://github.com/muhlba91/onyx-client/compare/v7.1.0...v7.1.1) (2023-08-29)


### Bug Fixes

* fix device_type enumeration ([d9483e7](https://github.com/muhlba91/onyx-client/commit/d9483e7217fc10625889ba98617bea2f22571dbb))


### Miscellaneous Chores

* **deps:** update dependency aiohttp to v3.8.5 ([3dd61c6](https://github.com/muhlba91/onyx-client/commit/3dd61c6ec91bec8a7e893ff44a6bc376dce630ef))
* **deps:** update dependency coverage to v7.3.0 ([5606fbc](https://github.com/muhlba91/onyx-client/commit/5606fbc5d63fdc026ee3506ceb2a118f31c7293b))

## [7.1.0](https://github.com/muhlba91/onyx-client/compare/v7.0.0...v7.1.0) (2023-07-19)


### Features

* **ci:** add build verification in pipeline ([ebb017f](https://github.com/muhlba91/onyx-client/commit/ebb017f472f275f84a44c3104bf1294e562e09dd))
* remove dynamic versioning and test pypi publishing ([f4d6810](https://github.com/muhlba91/onyx-client/commit/f4d6810a18ea2987fbe643d1e5584e929c0a024e))


### Bug Fixes

* add missing device types and shutter configuration ([43331f2](https://github.com/muhlba91/onyx-client/commit/43331f295b98b5d2101c00861e67342e6b1ea5c6))


### Miscellaneous Chores

* **ci:** fix release workflow ([771ebe0](https://github.com/muhlba91/onyx-client/commit/771ebe071f625389069c4b973909124bdb324f65))
* **ci:** fix release-please commit message ([4a3904b](https://github.com/muhlba91/onyx-client/commit/4a3904b5abe5f37ddae88d8f675a900446e72348))
* **ci:** leverage pypi trusted publishers ([0439942](https://github.com/muhlba91/onyx-client/commit/04399424465d0b930a542d8b103b66bd44b9ad2e))
* **deps:** update dependency black to v23.7.0 ([3054798](https://github.com/muhlba91/onyx-client/commit/3054798fe0d1d948991a1188854bb099636dceec))
* **deps:** update dependency pre-commit to v3.3.3 ([0106403](https://github.com/muhlba91/onyx-client/commit/0106403c99ec2d5a96d6d84ad34c59fc3f4dd50a))
* **deps:** update dependency pytest to v7.3.2 ([f841806](https://github.com/muhlba91/onyx-client/commit/f84180629c6fd07ae5bb5302fb3ff70be14fd20e))
* **deps:** update dependency pytest to v7.4.0 ([e019b0f](https://github.com/muhlba91/onyx-client/commit/e019b0f82d19f320f8f2c6661a4eddae7b701f21))
* **deps:** update dependency pytest-asyncio to v0.21.1 ([6b2919c](https://github.com/muhlba91/onyx-client/commit/6b2919c1e6caf424f746450ad05ab8243dcf5bf1))
* replace standard-version with release-please ([b747f7c](https://github.com/muhlba91/onyx-client/commit/b747f7c28ee1bd06385b19866210e872f6f273d1))

## [7.0.0](https://github.com/muhlba91/onyx-client/compare/v6.1.0...v7.0.0) (2023-06-08)


### ⚠ BREAKING CHANGES

* upgrades python to 3.11

### Features

* **ci:** update coverage to v7; use coveralls github action ([eccc20d](https://github.com/muhlba91/onyx-client/commit/eccc20d48246c5e7b584b6e3f550f2222290d059))
* update dependencies ([343543b](https://github.com/muhlba91/onyx-client/commit/343543bd9f38f2d6cc8c86fdca5b1f26b9ba9d01))
* upgrade to python 3.11 ([444b6a2](https://github.com/muhlba91/onyx-client/commit/444b6a2a270e7831d41575fd91b6c46e87a4ebdc))


### Bug Fixes

* **ci:** fix renovate commit message ([e10e528](https://github.com/muhlba91/onyx-client/commit/e10e528ae0fee477d1f3802ddb78e5d059e3f802))

## [6.1.0](https://github.com/muhlba91/onyx-client/compare/v6.0.0...v6.1.0) (2023-05-29)


### Features

* update dependencies ([9d997cd](https://github.com/muhlba91/onyx-client/commit/9d997cdca56bb78c86ef3a622a3efd76c6b4e6dc))

## [6.0.0](https://github.com/muhlba91/onyx-client/compare/v5.0.1...v6.0.0) (2023-03-24)


### ⚠ BREAKING CHANGES

* downgrade to python 3.10

### Features

* revert upgrade to python 3.11 ([9a532b2](https://github.com/muhlba91/onyx-client/commit/9a532b2c7f96ffa891043ea8c95c74c03dbf12c6))

### [5.0.1](https://github.com/muhlba91/onyx-client/compare/v5.0.0...v5.0.1) (2023-03-02)


### Bug Fixes

* fix versioning ([7fbf6dd](https://github.com/muhlba91/onyx-client/commit/7fbf6dd85e9fd909b0f525f2ab8eee7e22752202))

## [5.0.0](https://github.com/muhlba91/onyx-client/compare/v4.0.1...v5.0.0) (2023-03-02)


### ⚠ BREAKING CHANGES

* update to python 3.11

### Features

* update dependencies ([cf0c45a](https://github.com/muhlba91/onyx-client/commit/cf0c45a9f594ac8f18bf1f8fc496cc5ffc4fbf3a))

### [4.0.1](https://github.com/muhlba91/onyx-client/compare/v4.0.0...v4.0.1) (2022-07-08)


### Bug Fixes

* update min python version to 3.9 ([1c27d89](https://github.com/muhlba91/onyx-client/commit/1c27d89b7a0947f1a46b406fdd9978a6e35e8f40))
* update min python version to 3.9 ([db399ab](https://github.com/muhlba91/onyx-client/commit/db399ab77be7ded714f7ffc1e22f3ec99ead1472))

## [4.0.0](https://github.com/muhlba91/onyx-client/compare/v3.1.2...v4.0.0) (2022-07-08)


### ⚠ BREAKING CHANGES

* remove brotlipy dependency

### Features

* **ci:** add snyk monitor ([d4c8877](https://github.com/muhlba91/onyx-client/commit/d4c8877c2beb8cb76dbe01835d469d79981dbe13))
* update dependencies; use python 3.10 for testing ([ab4c55e](https://github.com/muhlba91/onyx-client/commit/ab4c55ef6ca07c278c66d55fed6e38a831c3f627))


### Bug Fixes

* **ci:** add remote repo url to snyk ([de3f739](https://github.com/muhlba91/onyx-client/commit/de3f739944c150a634eef8c94a07b9a7e74b079e))
* **ci:** fix python version ([ebbf387](https://github.com/muhlba91/onyx-client/commit/ebbf387c84eada8d360b005b541bf1625efd545c))
* **ci:** remove branch modifier for snyk ([5ae9172](https://github.com/muhlba91/onyx-client/commit/5ae9172521219e0d6b856bdb93e3180f700fa994))

### [3.1.2](https://github.com/muhlba91/onyx-client/compare/v3.1.1...v3.1.2) (2022-01-16)

### [3.1.1](https://github.com/muhlba91/onyx-client/compare/v3.1.0...v3.1.1) (2021-11-24)

## [3.1.0](https://github.com/muhlba91/onyx-client/compare/v3.0.4...v3.1.0) (2021-11-24)


### Features

* add switch device; [#11](https://github.com/muhlba91/onyx-client/issues/11) ([c7477bd](https://github.com/muhlba91/onyx-client/commit/c7477bdb35de5f83ae8eb846b5cecba51122705d))
* refactor client class; fix [#10](https://github.com/muhlba91/onyx-client/issues/10) ([8a052b6](https://github.com/muhlba91/onyx-client/commit/8a052b6fd3a9716171b5a99a07814fdb7e5352e2))


### Bug Fixes

* add new click device type; do not rely on properties; fix [#8](https://github.com/muhlba91/onyx-client/issues/8) ([fa039fc](https://github.com/muhlba91/onyx-client/commit/fa039fcdb9b66486b2c495926dec5458c6c62e05))
* merge in branch next ([462852e](https://github.com/muhlba91/onyx-client/commit/462852e0fb1eefc94eb62110b36efdf362aa0a82))
* remove dependency on properties being present ([59c4f2a](https://github.com/muhlba91/onyx-client/commit/59c4f2a249fc5dfedad40f46ab900986d31dc814))

### [3.0.4](https://github.com/muhlba91/onyx-client/compare/v3.0.3...v3.0.4) (2021-11-22)


### Bug Fixes

* detect device types correctly ([c5285c0](https://github.com/muhlba91/onyx-client/commit/c5285c0b0fb6d3a3acff61dfebdb223a428ff3d8))

### [3.0.3](https://github.com/muhlba91/onyx-client/compare/v3.0.2...v3.0.3) (2021-11-22)


### Bug Fixes

* handle none types on dicts ([96c4676](https://github.com/muhlba91/onyx-client/commit/96c467609756fd5233dff0591bd117d77c6c6ce5))

### [3.0.2](https://github.com/muhlba91/onyx-client/compare/v3.0.1...v3.0.2) (2021-11-22)


### Bug Fixes

* add new click device type; do not rely on properties; fix [#8](https://github.com/muhlba91/onyx-client/issues/8) ([9e92a1c](https://github.com/muhlba91/onyx-client/commit/9e92a1c15f27aea6b2a7c1ba5c43f32d362f32a8))
* remove dependency on properties being present ([3dac7a4](https://github.com/muhlba91/onyx-client/commit/3dac7a4afffb079095d9c7a078da0acadf3150ed))

### [3.0.1](https://github.com/muhlba91/onyx-client/compare/v3.0.0...v3.0.1) (2021-11-22)

## [3.0.0](https://github.com/muhlba91/onyx-client/compare/v2.5.0...v3.0.0) (2021-11-22)


### ⚠ BREAKING CHANGES

* uses Hella API v3

### Features

* bump version to use v3 ([251f63f](https://github.com/muhlba91/onyx-client/commit/251f63fa680453117cadbd799a2e494eeb61817b))


### Bug Fixes

* fix event streaming ([60f3eae](https://github.com/muhlba91/onyx-client/commit/60f3eae6f3bec563a15a467dcc1907594969800d))
* fix line length ([28a56f6](https://github.com/muhlba91/onyx-client/commit/28a56f6494bd27120b65755f2f583e45fc26b7c2))
* fix mapping of animations ([1ddea91](https://github.com/muhlba91/onyx-client/commit/1ddea910fd167cf38447c487d19a8cf81d143469))
* remove print statements ([f267b8c](https://github.com/muhlba91/onyx-client/commit/f267b8ccf66bad8afea4f76dbf81473198bc19b4))
* remove print statements ([5b14d2a](https://github.com/muhlba91/onyx-client/commit/5b14d2ab47534c92e063f21f2ab9715e3ef22210))
* support partial updates of animations ([7eafab3](https://github.com/muhlba91/onyx-client/commit/7eafab3f53d2173912e5bcdb0d8f7658fa5883f0))

## [2.5.0](https://github.com/muhlba91/onyx-client/compare/v2.4.0...v2.5.0) (2021-11-21)


### Features

* upgrade to API v3; fix [#5](https://github.com/muhlba91/onyx-client/issues/5) ([be1b1c3](https://github.com/muhlba91/onyx-client/commit/be1b1c39ca7472251e8243917480270de4f2eae7))

## [2.4.0](https://github.com/muhlba91/onyx-client/compare/v2.3.1...v2.4.0) (2021-02-14)


### Features

* add events endpoint, fix [#4](https://github.com/muhlba91/onyx-client/issues/4) ([5331c71](https://github.com/muhlba91/onyx-client/commit/5331c71dedbe839d8ca93b012afd612e2854a7b8))
* add update_with method to devices ([5e01c11](https://github.com/muhlba91/onyx-client/commit/5e01c11bf6e9221d6f42a5aa61eaab0d1ea767cc))

### [2.3.1](https://github.com/muhlba91/onyx-client/compare/v2.3.0...v2.3.1) (2021-02-12)


### Bug Fixes

* fix parsing of boolean values ([1bb9717](https://github.com/muhlba91/onyx-client/commit/1bb9717a2f1da871e6562d006f6b69d319e5b75c))

## [2.3.0](https://github.com/muhlba91/onyx-client/compare/v2.2.0...v2.3.0) (2021-02-12)


### Features

* add switch button and drive direction ([f378d96](https://github.com/muhlba91/onyx-client/commit/f378d9635cf0f26924242e860666793cef3b9a0c))

## [2.2.0](https://github.com/muhlba91/onyx-client/compare/v2.1.0...v2.2.0) (2021-02-10)


### Features

* add drivetime and rotationtime properties to shutters ([9ac7e95](https://github.com/muhlba91/onyx-client/commit/9ac7e9511caa0578684240c2e0d6890a375f13bc))

## [2.1.0](https://github.com/muhlba91/onyx-client/compare/v2.0.2...v2.1.0) (2021-02-09)


### Features

* downgrade python to 3.8 ([e140367](https://github.com/muhlba91/onyx-client/commit/e140367bb6138c7ed33e0712d1fa9d233fbf9c1d))


### Bug Fixes

* downgrade to python 3.8 ([dec639b](https://github.com/muhlba91/onyx-client/commit/dec639bf42ccfd6ba06478d8179b5606c3544e34))

### [2.0.2](https://github.com/muhlba91/onyx-client/compare/v2.0.1...v2.0.2) (2021-02-09)


### Bug Fixes

* fix changelog duplication ([5e2c02e](https://github.com/muhlba91/onyx-client/commit/5e2c02e6e5d56664e5e4f71b6be0827daf7d118b))

### [2.0.1](https://github.com/muhlba91/onyx-client/compare/v2.0.0...v2.0.1) (2021-02-09)


### Bug Fixes

* fix versioning ([5ef5810](https://github.com/muhlba91/onyx-client/commit/5ef581036f472bcf1874e33ba4e962c8d20c3b97))
* remove package json from versioning ([49e6506](https://github.com/muhlba91/onyx-client/commit/49e6506c56909dff64dc1b632c096ee237a695b5))

## 2.0.0 (2021-02-09)


### ⚠ BREAKING CHANGES

* update to api v2, include new properties and positions

### Features

* update to api v2, include new properties and positions ([0b1c497](https://github.com/muhlba91/onyx-client/commit/0b1c497262a91c7b61b65eb9f7c315eac16522d9))


### Bug Fixes

* json payload for post requests ([f41e0be](https://github.com/muhlba91/onyx-client/commit/f41e0bea5a496b0cdad2b697ce483bcd8002a716))
