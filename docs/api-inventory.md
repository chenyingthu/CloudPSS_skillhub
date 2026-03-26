# CloudPSS SDK Inventory

- Generated at: 2026-03-16 12:02:16
- SDK version: `4.5.28`
- Source SDK root: `/home/chenying/anaconda3/lib/python3.12/site-packages/cloudpss`
- Scope: `Model`, `Job`, `ModelRevision`, `Component`, `EMTResult`, `PowerFlowResult`

## Summary

| Class | Members | Documented | Examples | Tests | Verified |
|------|---------|------------|----------|-------|----------|
| Model | 30 | 26 | 26 | 19 | 16 |
| Job | 10 | 9 | 9 | 9 | 6 |
| EMTResult | 24 | 14 | 14 | 15 | 14 |
| ModelRevision | 5 | 5 | 5 | 5 | 5 |
| Component | 1 | 1 | 1 | 1 | 0 |
| PowerFlowResult | 14 | 4 | 4 | 5 | 4 |

## P0 Gaps

No gaps in this priority band.

## P1 Gaps

| API | Missing Docs | Missing Example | Missing Test | Verification |
|-----|--------------|-----------------|--------------|--------------|
| Model.iesSimulationRun | yes | yes | yes | none |
| Model.runIESEnergyStoragePlan | yes |  | yes | none |
| Model.runIESLoadPrediction | yes |  | yes | none |
| Model.runIESPowerFlow | yes |  | yes | none |
| Model.runThreePhasePowerFlow |  | yes | yes | none |

## Full Inventory

### Model

- Module: `cloudpss.model.model`
- API doc: `docs/api-reference/model-api.md`

| Member | Kind | Priority | Docs | Example | Test | Verification | Source |
|--------|------|----------|------|---------|------|--------------|--------|
| `addComponent(self, definition, label, args, pins, canvas=None, position=None, size=None)` | method | P0 | Y | Y | Y | unit | `cloudpss/model/model.py:119` |
| `dump(model, file, format='yaml', compress='gzip')` | method | P0 | Y | Y | Y | unit | `cloudpss/model/model.py:406` |
| `fetch(rid, **kwargs)` | method | P0 | Y | Y | Y | integration | `cloudpss/model/model.py:340` |
| `fetchMany(name=None, cursor=[], pageSize=10, owner=None, **kwargs)` | method | P0 | Y | Y | Y | integration | `cloudpss/model/model.py:300` |
| `fetchTopology(self, implementType=None, config=None, maximumDepth=None, **kwargs)` | method | P0 | Y | Y | Y | unit | `cloudpss/model/model.py:590` |
| `getAllComponents(self) -> dict` | method | P0 | Y | Y | Y | unit | `cloudpss/model/model.py:103` |
| `getComponentByKey(self, componentKey: str)` | method | P0 | Y | Y | Y | unit | `cloudpss/model/model.py:186` |
| `getComponentsByRid(self, rid: str)` | method | P0 | Y | Y | Y | unit | `cloudpss/model/model.py:159` |
| `load(filePath, format='yaml')` | method | P0 | Y | Y | Y | unit | `cloudpss/model/model.py:385` |
| `removeComponent(self, key)` | method | P0 | Y | Y | Y | unit | `cloudpss/model/model.py:132` |
| `run(self, job=None, config=None, name=None, **kwargs)` | method | P0 | Y | Y | Y | unit | `cloudpss/model/model.py:357` |
| `runEMT(self, job=None, config=None, **kwargs) -> cloudpss.job.job.Job[cloudpss.job.result.EMTResult.EMTResult]` | method | P0 | Y | Y | Y | integration | `cloudpss/model/model.py:663` |
| `runPowerFlow(self, job=None, config=None, **kwargs) -> cloudpss.runner.runner.Runner[cloudpss.job.result.PowerFlowResult.PowerFlowResult]` | method | P0 | Y | Y | Y | integration | `cloudpss/model/model.py:704` |
| `runSFEMT(self, job=None, config=None, **kwargs) -> cloudpss.runner.runner.Runner[cloudpss.job.result.EMTResult.EMTResult]` | method | P0 | Y | Y | Y | unit | `cloudpss/model/model.py:684` |
| `save(self, key=None)` | method | P0 | Y | Y | Y | unit | `cloudpss/model/model.py:423` |
| `updateComponent(self, key, **kwargs)` | method | P0 | Y | Y | Y | unit | `cloudpss/model/model.py:145` |
| `iesSimulationRun(self, job=None, config=None, name=None, **kwargs)` | method | P1 | N | N | N | none | `cloudpss/model/model.py:382` |
| `runIESEnergyStoragePlan(self, job=None, config=None, **kwargs) -> cloudpss.job.job.Job[cloudpss.runner.result.IESResult]` | method | P1 | N | Y | N | none | `cloudpss/model/model.py:784` |
| `runIESLoadPrediction(self, job=None, config=None, **kwargs) -> cloudpss.job.job.Job[cloudpss.runner.result.IESResult]` | method | P1 | N | Y | N | none | `cloudpss/model/model.py:744` |
| `runIESPowerFlow(self, job=None, config=None, **kwargs) -> cloudpss.job.job.Job[cloudpss.runner.result.IESResult]` | method | P1 | N | Y | N | none | `cloudpss/model/model.py:764` |
| `runThreePhasePowerFlow(self, job=None, config=None, **kwargs) -> cloudpss.job.job.Job[cloudpss.job.result.PowerFlowResult.PowerFlowResult]` | method | P1 | Y | N | N | none | `cloudpss/model/model.py:724` |
| `addConfig(self, config)` | method | reference | Y | Y | N | none | `cloudpss/model/model.py:286` |
| `addJob(self, job: dict)` | method | reference | Y | Y | N | none | `cloudpss/model/model.py:238` |
| `create(model, **kwargs)` | method | reference | Y | Y | Y | none | `cloudpss/model/model.py:466` |
| `createConfig(self, name)` | method | reference | Y | Y | N | none | `cloudpss/model/model.py:268` |
| `createJob(self, jobType: str, name: str)` | method | reference | Y | Y | N | none | `cloudpss/model/model.py:219` |
| `getModelConfig(self, name)` | method | reference | Y | N | N | none | `cloudpss/model/model.py:250` |
| `getModelJob(self, name)` | method | reference | Y | Y | N | none | `cloudpss/model/model.py:201` |
| `toJSON(self)` | method | reference | Y | Y | Y | none | `cloudpss/model/model.py:95` |
| `update(model, **kwargs)` | method | reference | Y | N | Y | none | `cloudpss/model/model.py:524` |
### Job

- Module: `cloudpss.job.job`
- API doc: `docs/api-reference/job-api.md`

| Member | Kind | Priority | Docs | Example | Test | Verification | Source |
|--------|------|----------|------|---------|------|--------------|--------|
| `abort(self, timeout=3, **kwargs)` | method | P0 | Y | Y | Y | unit | `cloudpss/job/job.py:276` |
| `create(revisionHash, job, config, name=None, rid=None, policy=None, **kwargs)` | method | P0 | Y | Y | Y | none | `cloudpss/job/job.py:170` |
| `dump(job, file, format='yaml', compress='gzip')` | method | P0 | Y | Y | Y | none | `cloudpss/job/job.py:198` |
| `fetch(id, **kwargs)` | method | P0 | Y | Y | Y | integration | `cloudpss/job/job.py:92` |
| `load(file, format='yaml')` | method | P0 | Y | Y | Y | none | `cloudpss/job/job.py:194` |
| `read(self, receiver=None, **kwargs)` | method | P0 | Y | Y | Y | unit | `cloudpss/job/job.py:204` |
| `result(self) -> ~T` | property | P0 | Y | Y | Y | integration | `cloudpss/job/job.py:251` |
| `status(self)` | method | P0 | Y | Y | Y | integration | `cloudpss/job/job.py:229` |
| `write(self, sender=None, **kwargs) -> cloudpss.job.messageStreamSender.MessageStreamSender` | method | P0 | Y | Y | Y | unit | `cloudpss/job/job.py:217` |
| `close(self)` | method | reference | N | N | N | none | `cloudpss/job/job.py:295` |
### EMTResult

- Module: `cloudpss.job.result.EMTResult`
- API doc: `docs/api-reference/emtresult-api.md`

| Member | Kind | Priority | Docs | Example | Test | Verification | Source |
|--------|------|----------|------|---------|------|--------------|--------|
| `control(self, controlParam, eventTime='-1', eventTimeType='1')` | method | P0 | Y | Y | Y | unit | `cloudpss/job/result/EMTResult.py:222` |
| `getMessagesByKey(self, key)` | method | P0 | Y | Y | Y | unit | `cloudpss/job/result/result.py:73` |
| `getPlot(self, index: int)` | method | P0 | Y | Y | Y | unit+integration | `cloudpss/job/result/EMTResult.py:72` |
| `getPlotChannelData(self, index, channelName)` | method | P0 | Y | Y | Y | unit+integration | `cloudpss/job/result/EMTResult.py:102` |
| `getPlotChannelNames(self, index)` | method | P0 | Y | Y | Y | unit+integration | `cloudpss/job/result/EMTResult.py:85` |
| `getPlots(self)` | method | P0 | Y | Y | Y | unit+integration | `cloudpss/job/result/EMTResult.py:47` |
| `goto(self, step)` | method | P0 | Y | Y | Y | unit | `cloudpss/job/result/EMTResult.py:129` |
| `loadSnapshot(self, snapshotNumber, log='加载断面成功')` | method | P0 | Y | Y | Y | unit | `cloudpss/job/result/EMTResult.py:216` |
| `monitor(self, monitorParam, eventTime='-1', eventTimeType='1')` | method | P0 | Y | Y | Y | unit | `cloudpss/job/result/EMTResult.py:245` |
| `next(self)` | method | P0 | Y | Y | Y | unit | `cloudpss/job/result/EMTResult.py:122` |
| `saveSnapshot(self, snapshotNumber, log='保存断面成功')` | method | P0 | Y | Y | Y | unit | `cloudpss/job/result/EMTResult.py:211` |
| `send(self, message=None)` | method | P0 | Y | Y | Y | unit | `cloudpss/job/result/EMTResult.py:148` |
| `stopSimulation(self)` | method | P0 | Y | Y | Y | unit | `cloudpss/job/result/EMTResult.py:180` |
| `writeShm(self, path, buffer, offset)` | method | P0 | Y | Y | Y | unit | `cloudpss/job/result/EMTResult.py:139` |
| `db(self)` | property | reference | N | N | N | none | `cloudpss/job/result/result.py:161` |
| `getLogs(self)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:127` |
| `getMessage(self, index)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:106` |
| `getMessageLength(self)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:144` |
| `getMessages(self)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:118` |
| `getMessagesByType(self, type)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:90` |
| `modify(self, data, model)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:59` |
| `pop(self, index=-1)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:171` |
| `receive(self)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:36` |
| `waitFor(self, timeOut=9223372036854775807)` | method | reference | N | N | Y | none | `cloudpss/job/result/result.py:153` |
### ModelRevision

- Module: `cloudpss.model.revision`
- API doc: `docs/api-reference/revision-api.md`

| Member | Kind | Priority | Docs | Example | Test | Verification | Source |
|--------|------|----------|------|---------|------|--------------|--------|
| `create(revision, parentHash=None, **kwargs)` | method | P0 | Y | Y | Y | unit | `cloudpss/model/revision.py:87` |
| `fetchTopology(self, implementType, config, maximumDepth, **kwargs)` | method | P0 | Y | Y | Y | integration | `cloudpss/model/revision.py:111` |
| `getImplements(self)` | method | P0 | Y | Y | Y | unit | `cloudpss/model/revision.py:54` |
| `run(self, job, config, name=None, policy=None, stop_on_entry=None, rid=None, **kwargs)` | method | P0 | Y | Y | Y | integration | `cloudpss/model/revision.py:65` |
| `toJSON(self)` | method | P0 | Y | Y | Y | unit | `cloudpss/model/revision.py:45` |
### Component

- Module: `cloudpss.model.implements.component`
- API doc: `docs/api-reference/component-api.md`

| Member | Kind | Priority | Docs | Example | Test | Verification | Source |
|--------|------|----------|------|---------|------|--------------|--------|
| `toJSON(self)` | method | P0 | Y | Y | Y | none | `cloudpss/model/implements/component.py:23` |
### PowerFlowResult

- Module: `cloudpss.job.result.PowerFlowResult`
- API doc: `docs/api-reference/powerflow-result-api.md`

| Member | Kind | Priority | Docs | Example | Test | Verification | Source |
|--------|------|----------|------|---------|------|--------------|--------|
| `getBranches(self)` | method | P0 | Y | Y | Y | unit+integration | `cloudpss/job/result/PowerFlowResult.py:43` |
| `getBuses(self)` | method | P0 | Y | Y | Y | unit+integration | `cloudpss/job/result/PowerFlowResult.py:17` |
| `getMessagesByKey(self, key)` | method | P0 | Y | Y | Y | unit | `cloudpss/job/result/result.py:73` |
| `powerFlowModify(self, model)` | method | P0 | Y | Y | Y | unit | `cloudpss/job/result/PowerFlowResult.py:70` |
| `db(self)` | property | reference | N | N | N | none | `cloudpss/job/result/result.py:161` |
| `getLogs(self)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:127` |
| `getMessage(self, index)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:106` |
| `getMessageLength(self)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:144` |
| `getMessages(self)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:118` |
| `getMessagesByType(self, type)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:90` |
| `modify(self, data, model)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:59` |
| `pop(self, index=-1)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:171` |
| `receive(self)` | method | reference | N | N | N | none | `cloudpss/job/result/result.py:36` |
| `waitFor(self, timeOut=9223372036854775807)` | method | reference | N | N | Y | none | `cloudpss/job/result/result.py:153` |

## Notes

- `documented` means the member name appears in the class-specific API markdown file.
- `example_exists` means the member name appears in at least one file under `examples/`.
- `test_exists` means the member name appears in at least one file under `tests/`.
- `verification` is curated from the current trusted test suite, not inferred from raw string matches.
